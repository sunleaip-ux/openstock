import json, os, subprocess
from datetime import datetime
from config import GITHUB_USERNAME, GITHUB_REPO, GITHUB_TOKEN, GITHUB_EMAIL

class DashboardGenerator:
    @staticmethod
    def generate(recommended_stocks, market_trend):
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        stocks_json = json.dumps(recommended_stocks, ensure_ascii=False)
        html_template = f"""<!DOCTYPE html><html><head><meta charset='UTF-8'><title>OpenStock AI</title><script src='https://cdn.tailwindcss.com'></script><script src='https://cdn.jsdelivr.net/npm/chart.js'></script><style>body{{background-color:#0f172a;color:#e2e8f0;}} .stock-card{{background-color:#1e293b;border:1px solid #334155;}}</style></head><body class='p-8'><div class='max-w-6xl mx-auto'><h1 class='text-4xl font-bold text-white mb-8'>📈 OpenStock AI</h1><div id='stock-container' class='grid grid-cols-1 md:grid-cols-3 gap-6'></div></div><script>const stocks={stocks_json}; const container=document.getElementById('stock-container'); stocks.forEach((stock, index)=>{{ const card=document.createElement('div'); card.className='stock-card p-6 rounded-2xl'; card.innerHTML=`<h2 class='text-2xl font-bold text-white mb-4'>${{stock.name}} (${{stock.id}}) <span class='text-sky-400 ml-2'>${{stock.score}}</span></h2><div class='h-48 mb-4'><canvas id='chart-${{index}}'></canvas></div><div class='text-sm text-slate-300 mb-4'>${{stock.reasons.map(r=>`<div>✅ ${{r}}</div>`).join('')}}</div><div class='p-2 bg-slate-800 rounded text-xs italic text-sky-400'>${{stock.ai_insight}}</div>`; container.appendChild(card); const ctx=document.getElementById(`chart-${{index}}`).getContext('2d'); new Chart(ctx, {{type:'radar', data:{{labels:['基本面','技術面','籌碼面','消息面'], datasets:[{{data:stock.component_scores, borderColor:'#38bdf8', backgroundColor:'rgba(56,189,248,0.2)'}}]}}, options:{{scales:{{r:{{beginAtZero:true,max:100,ticks:{{display:false}}}}}}, plugins:{{legend:{{display:false}}}}}})}}); }});</script></body></html>"""
        with open("index.html", "w", encoding="utf-8") as f: f.write(html_template)
        return "index.html"
    @staticmethod
    def deploy():
        try:
            subprocess.run(["git", "config", "user.email", GITHUB_EMAIL], check=True)
            subprocess.run(["git", "config", "user.name", GITHUB_USERNAME], check=True)
            remote_url = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{GITHUB_REPO}.git"
            if not os.path.exists(".git"):
                subprocess.run(["git", "clone", remote_url, "."], check=True)
            subprocess.run(["git", "add", "index.html"], check=True)
            subprocess.run(["git", "commit", "-m", f"Update {datetime.now()}"], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            return True
        except: return False
