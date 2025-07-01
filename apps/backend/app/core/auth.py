"""
Clerk authentication middleware and utilities.
"""
from typing import Optional, Dict, Any
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
import jwt
from jwt import PyJWKClient

from app.core.config import settings
from app.core.database import get_db_dependency
from prisma import Prisma
from prisma.models import User


# Security scheme for OpenAPI documentation
security = HTTPBearer()


class ClerkAuth:
    """Handle Clerk authentication and token verification."""
    
    def __init__(self):
        self.clerk_secret_key = settings.CLERK_SECRET_KEY
        self.issuer = settings.CLERK_ISSUER
        
        # Initialize JWKS client for token verification
        jwks_url = f"{self.issuer}/.well-known/jwks.json"
        self.jwks_client = PyJWKClient(jwks_url)
    
    async def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verify Clerk JWT token and return decoded payload.
        
        Args:
            token: JWT token string
            
        Returns:
            Decoded token payload
            
        Raises:
            HTTPException: If token is invalid
        """
        try:
            # Get the signing key from Clerk's JWKS
            signing_key = self.jwks_client.get_signing_key_from_jwt(token)
            
            # Decode and verify the token
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                issuer=self.issuer,
                options={"verify_aud": False}  # Clerk tokens don't always have audience
            )
            
            return payload
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token verification failed: {str(e)}"
            )
    
    async def get_user_from_clerk(self, user_id: str) -> Dict[str, Any]:
        """
        Fetch user details from Clerk API.
        
        Args:
            user_id: Clerk user ID
            
        Returns:
            User data from Clerk
        """
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {self.clerk_secret_key}",
                "Content-Type": "application/json"
            }
            
            response = await client.get(
                f"https://api.clerk.com/v1/users/{user_id}",
                headers=headers
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to fetch user from Clerk"
                )
            
            return response.json()


# Create global auth instance
clerk_auth = ClerkAuth()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Prisma = Depends(get_db_dependency)
) -> User:
    """
    Get current user from JWT token.
    
    This dependency:
    1. Verifies the JWT token
    2. Extracts user ID from token
    3. Fetches or creates user in database
    4. Returns the user object
    
    Args:
        credentials: Bearer token from request
        db: Database connection
        
    Returns:
        User object from database
        
    Raises:
        HTTPException: If authentication fails
    """
    # Verify token
    token_data = await clerk_auth.verify_token(credentials.credentials)
    
    # Extract user ID from token
    clerk_user_id = token_data.get("sub")
    if not clerk_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: no user ID"
        )
    
    # Check if user exists in database
    user = await db.user.find_unique(where={"clerkId": clerk_user_id})
    
    # If user doesn't exist, fetch from Clerk and create
    if not user:
        clerk_user = await clerk_auth.get_user_from_clerk(clerk_user_id)
        
        # Extract user data
        email = clerk_user.get("email_addresses", [{}])[0].get("email_address", "")
        phone = clerk_user.get("phone_numbers", [{}])[0].get("phone_number", "")
        
        # Determine user role (check if user has admin role in Clerk)
        public_metadata = clerk_user.get("public_metadata", {})
        role = "ADMIN" if public_metadata.get("role") == "admin" else "CUSTOMER"
        
        # Create user in database
        user = await db.user.create(
            data={
                "clerkId": clerk_user_id,
                "email": email,
                "name": f"{clerk_user.get('first_name', '')} {clerk_user.get('last_name', '')}".strip(),
                "phone": phone,
                "role": role
            }
        )
    
    return user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current user and verify they have admin role.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User object if admin
        
    Raises:
        HTTPException: If user is not admin
    """
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return current_user


async def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Prisma = Depends(get_db_dependency)
) -> Optional[User]:
    """
    Get current user if authenticated, otherwise return None.
    
    This is useful for endpoints that work for both authenticated
    and unauthenticated users but provide different data.
    
    Args:
        credentials: Optional bearer token
        db: Database connection
        
    Returns:
        User object or None
    """
    if not credentials:
        return None
    
    try:
        return await get_current_user(credentials, db)
    except HTTPException:
        return None