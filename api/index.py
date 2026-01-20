
import os
import sys

# 將當前目錄加入 path，確保能 import api.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import app

# Vercel 需要 application 變數
application = app

if __name__ == "__main__":
    app.run()
