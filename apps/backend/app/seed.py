"""
Database seed script for Coffee Shop application.
Populates the database with initial categories and coffee items.
"""
import asyncio
from datetime import datetime
from prisma import Prisma
import sys


# Seed data
CATEGORIES = [
    {
        "id": "all",
        "name": "所有",
        "description": "所有咖啡",
        "sortOrder": 0,
        "active": True
    },
    {
        "id": "espresso",
        "name": "浓缩咖啡",
        "description": "意式浓缩咖啡系列",
        "sortOrder": 1,
        "active": True
    },
    {
        "id": "filter",
        "name": "手冲咖啡",
        "description": "精品手冲咖啡",
        "sortOrder": 2,
        "active": True
    },
    {
        "id": "coldbrew",
        "name": "冷萃咖啡",
        "description": "冷萃和冰咖啡",
        "sortOrder": 3,
        "active": True
    },
    {
        "id": "specialty",
        "name": "特色饮品",
        "description": "特色创意咖啡",
        "sortOrder": 4,
        "active": True
    }
]

COFFEE_ITEMS = [
    # Espresso category
    {
        "name": "卡布奇诺",
        "description": "经典意式咖啡，奶泡绵密，带有简易坚果味",
        "price": 25.00,
        "categoryId": "espresso",
        "available": True,
        "imageUrl": "/images/cappuccino.jpg"
    },
    {
        "name": "拿铁咖啡",
        "description": "浓郁咖啡与丝滑牛奶的完美融合",
        "price": 28.00,
        "categoryId": "espresso",
        "available": True,
        "imageUrl": "/images/latte.jpg"
    },
    {
        "name": "摩卡咖啡",
        "description": "巧克力与咖啡的甜蜜邂逅",
        "price": 30.00,
        "categoryId": "espresso",
        "available": True,
        "imageUrl": "/images/mocha.jpg"
    },
    {
        "name": "焦糖玛奇朵",
        "description": "香草糖浆、蒸奶、浓缩咖啡与焦糖的层次享受",
        "price": 32.00,
        "categoryId": "espresso",
        "available": True,
        "imageUrl": "/images/caramel-macchiato.jpg"
    },
    {
        "name": "馥芮白",
        "description": "澳洲经典，微奶泡与双份浓缩的黄金比例",
        "price": 26.00,
        "categoryId": "espresso",
        "available": True,
        "imageUrl": "/images/flat-white.jpg"
    },
    
    # Filter coffee category
    {
        "name": "手冲单品",
        "description": "精选单一产地咖啡豆，手工冲泡",
        "price": 35.00,
        "categoryId": "filter",
        "available": True,
        "imageUrl": "/images/pour-over.jpg"
    },
    {
        "name": "美式咖啡",
        "description": "经典黑咖啡，口感纯净",
        "price": 22.00,
        "categoryId": "filter",
        "available": True,
        "imageUrl": "/images/americano.jpg"
    },
    
    # Cold brew category
    {
        "name": "冷萃咖啡",
        "description": "12小时低温萃取，口感顺滑",
        "price": 28.00,
        "categoryId": "coldbrew",
        "available": True,
        "imageUrl": "/images/cold-brew.jpg"
    },
    {
        "name": "冰拿铁",
        "description": "夏日清凉之选，浓缩咖啡配冰牛奶",
        "price": 30.00,
        "categoryId": "coldbrew",
        "available": True,
        "imageUrl": "/images/iced-latte.jpg"
    },
    
    # Specialty category
    {
        "name": "抹茶拿铁",
        "description": "日式抹茶粉配香草牛奶",
        "price": 32.00,
        "categoryId": "specialty",
        "available": True,
        "imageUrl": "/images/matcha-latte.jpg"
    },
    {
        "name": "芋头拿铁",
        "description": "紫色梦幻，芋头与咖啡的创意结合",
        "price": 30.00,
        "categoryId": "specialty",
        "available": True,
        "imageUrl": "/images/taro-latte.jpg"
    },
    {
        "name": "红色天鹅绒拿铁",
        "description": "红丝绒蛋糕风味，配有巧克力",
        "price": 34.00,
        "categoryId": "specialty",
        "available": True,
        "imageUrl": "/images/red-velvet-latte.jpg"
    }
]


async def clear_database(db: Prisma):
    """Clear existing data from database."""
    print("🗑️  Clearing existing data...")
    
    # Delete in order to respect foreign key constraints
    await db.review.delete_many()
    await db.orderitem.delete_many()
    await db.payment.delete_many()
    await db.order.delete_many()
    await db.rewards.delete_many()
    await db.coffee.delete_many()
    await db.category.delete_many()
    await db.user.delete_many()
    
    print("✅ Database cleared")


async def seed_categories(db: Prisma):
    """Seed categories."""
    print("\n📁 Seeding categories...")
    
    for category in CATEGORIES:
        existing = await db.category.find_unique(where={"id": category["id"]})
        if not existing:
            await db.category.create(data=category)
            print(f"  ✅ Created category: {category['name']}")
        else:
            print(f"  ⏭️  Category already exists: {category['name']}")
    
    print(f"✅ Seeded {len(CATEGORIES)} categories")


async def seed_coffee_items(db: Prisma):
    """Seed coffee items."""
    print("\n☕ Seeding coffee items...")
    
    created_count = 0
    for item in COFFEE_ITEMS:
        # Check if item already exists
        existing = await db.coffee.find_first(
            where={
                "name": item["name"],
                "categoryId": item["categoryId"]
            }
        )
        
        if not existing:
            await db.coffee.create(data=item)
            print(f"  ✅ Created coffee: {item['name']} - ¥{item['price']}")
            created_count += 1
        else:
            print(f"  ⏭️  Coffee already exists: {item['name']}")
    
    print(f"✅ Seeded {created_count} new coffee items")


async def print_summary(db: Prisma):
    """Print summary of seeded data."""
    print("\n📊 Database Summary:")
    
    # Count records
    category_count = await db.category.count()
    coffee_count = await db.coffee.count()
    
    print(f"  - Categories: {category_count}")
    print(f"  - Coffee Items: {coffee_count}")
    
    # Show sample items by category
    print("\n📋 Sample items by category:")
    categories = await db.category.find_many(order={"sortOrder": "asc"})
    
    for category in categories:
        if category.id == "all":
            continue
            
        coffees = await db.coffee.find_many(
            where={"categoryId": category.id},
            take=2
        )
        
        if coffees:
            print(f"\n  {category.name}:")
            for coffee in coffees:
                print(f"    - {coffee.name}: ¥{coffee.price}")


async def main():
    """Main seed function."""
    print("🌱 Starting Coffee Shop Database Seed")
    print("=" * 50)
    
    # Connect to database
    db = Prisma()
    await db.connect()
    
    try:
        # Ask user if they want to clear existing data
        if len(sys.argv) > 1 and sys.argv[1] == "--clear":
            await clear_database(db)
        
        # Seed data
        await seed_categories(db)
        await seed_coffee_items(db)
        
        # Print summary
        await print_summary(db)
        
        print("\n✨ Database seeding completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {str(e)}")
        raise
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())