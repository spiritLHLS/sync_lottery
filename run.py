from fastapi import FastAPI
import uvicorn
from main import application



app = FastAPI(
    title='SYNCLOTTERY by spiritlhl',
    description='个人部署，请修改run.py文件部署',
    version='1.0.0',
    docs_url='/docs',
    redoc_url='/redocs',
)

#prefix后缀地址
app.include_router(application, prefix='/lottery', tags=['lottery'])#, prefix='/b'



if __name__ == '__main__':
    uvicorn.run('run:app', host='0.0.0.0', port=3333, reload=True, debug=True, workers=1)
