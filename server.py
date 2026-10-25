import os, json, urllib.request, urllib.error
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT=Path(__file__).resolve().parent
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(ROOT),**kwargs)
    def do_GET(self):
        if self.path == '/api/status':
            self.respond(200,{'online':bool(os.environ.get('DEEPSEEK_API_KEY'))}); return
        return super().do_GET()
    def do_POST(self):
        if self.path!='/api/chat': self.respond(404,{'error':'not found'});return
        key=os.environ.get('DEEPSEEK_API_KEY','').strip()
        if not key: self.respond(503,{'error':'未配置 DEEPSEEK_API_KEY，请使用演示模式或启动时配置环境变量'});return
        try:
            length=int(self.headers.get('Content-Length','0'))
            if length>80000: self.respond(413,{'error':'请求过大'});return
            body=json.loads(self.rfile.read(length))
            messages=body.get('messages',[])
            if not isinstance(messages,list) or len(messages)>45: raise ValueError('对话格式错误')
            clean=[]
            for m in messages:
                if m.get('role') not in ('system','user','assistant') or not isinstance(m.get('content'),str): raise ValueError('消息格式错误')
                clean.append({'role':m['role'],'content':m['content'][:12000]})
            req=urllib.request.Request('https://api.deepseek.com/chat/completions',data=json.dumps({'model':'deepseek-chat','messages':clean,'temperature':0.75,'max_tokens':1100,'stream':False},ensure_ascii=False).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+key},method='POST')
            try:
                with urllib.request.urlopen(req,timeout=65) as response: data=json.load(response)
            except urllib.error.HTTPError as e:
                self.respond(502,{'error':'DeepSeek 返回错误：'+str(e.code)});return
            self.respond(200,{'content':data['choices'][0]['message']['content']})
        except Exception as e: self.respond(500,{'error':str(e)[:200]})
    def respond(self,status,data):
        b=json.dumps(data,ensure_ascii=False).encode('utf-8');self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
if __name__=='__main__':
    port=int(os.environ.get('PORT','8765'))
    print(f'访问 http://localhost:{port} | DeepSeek: {"已配置" if os.environ.get("DEEPSEEK_API_KEY") else "未配置，使用本地演示"}')
    ThreadingHTTPServer(('127.0.0.1',port),Handler).serve_forever()
