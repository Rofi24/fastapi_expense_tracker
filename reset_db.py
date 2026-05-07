import asyncio
from sqlalchemy import text
from app.core.database import engine

async def nuke_database():
    print("MEMULAI PENGHAPUSAN TOTAL...")
    async with engine.begin() as conn:
        try:
            # Kita paksa hapus tabel pakai SQL mentah
            await conn.execute(text("DROP TABLE IF EXISTS transactions CASCADE;"))
            await conn.execute(text("DROP TABLE IF EXISTS users CASCADE;"))
            print("✅ BERHASIL: Tabel 'transactions' dan 'users' sudah rata dengan tanah!")
        except Exception as e:
            print(f"❌ GAGAL: {e}")

if __name__ == "__main__":
    asyncio.run(nuke_database())