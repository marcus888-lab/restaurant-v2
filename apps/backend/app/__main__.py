"""
Module entry point for running scripts.
"""
import sys

if len(sys.argv) > 1 and sys.argv[1] == "seed":
    from app.seed import main
    import asyncio
    asyncio.run(main())
else:
    print("Usage: python -m app <command>")
    print("Commands:")
    print("  seed - Seed the database with initial data")