from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from prisma import Prisma
from typing import Dict, Optional

prisma = Prisma()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await prisma.connect()
    yield

    await prisma.disconnect()

app = FastAPI(lifespan=lifespan)

# @app.on_event("startup")
# async def startup():
#     await prisma.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     await prisma.disconnect()

@app.get("/")
async def read_root() -> Dict[str, str]:
    return {
        "/{nama_wilayah}" : "mendapatkan kode wilayah (Kecamatan & Desa)",
        "/adm2/{nama_wilayah}" : "mendapatkan kode wilayah (Provinsi & Kabupaten)",
        "/kode/{kode_wilayah}" : "mendapatkan nama wilayah (Kecamatan & Desa)"
    }

@app.get("/{wilayah}")
async def get_wilayah(wilayah: str) -> str:
    try:
        result = await prisma.wilayah.find_many(
            where={
                "nama": wilayah
            },
            select={
                "kode": True,
                "nama": True
            }
        )

        if result and len(result) > 0:
            return result[0].kode
        return "Data tidak ditemukan"
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/adm2/{wilayah}")
async def get_adm2_wilayah(wilayah: str) -> str:
    try:
        result = await prisma.wilayah.find_many(
            where={
                "nama": wilayah.upper()
            },
            select={
                "kode": True,
                "nama": True
            }
        )

        if result and len(result) > 0:
            return result[0].kode
        return "Data tidak ditemukan"
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/kode/{kode}")
async def get_kode_wilayah(kode: str) -> str:
    try:
        result = await prisma.wilayah.find_many(
            where={
                "kode": kode
            },
            select={
                "kode": True,
                "nama": True
            }
        )

        if result and len(result) > 0:
            return result[0].nama
        return "Data tidak ditemukan"

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)