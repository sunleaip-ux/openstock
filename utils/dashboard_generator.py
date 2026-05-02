import os
import json
from datetime import datetime
from git import Repo

class DashboardGenerator:
    @staticmethod
    def generate(candidates, market_trend="Bullish"):
        # Ensure candidates is a list
        if not candidates:
            candidates = []
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # Robust HTML template with safe variable access
        html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenStock AI | 量化選股儀表板</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ background-color: #0f172a; color: #f8fafc; }}
        .glass {{ background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); }}
        .radar-container {{ position: relative; height: 250px; width: 250px; }}
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-6xl mx-auto">
        <header class="flex justify-between items-center mb-8">
            <div>
                <h1 class="text-3xl font-bold text-sky-400">OpenStock AI</h1>
                <p class="text-slate-400">量化選股分析報告 | 市場狀態: <span class="text-green-400">{market_trend}</span></p>
            </div>
            <div class="text-right">
                <p class="text-xs text-slate-500 uppercase">Last Update</p>
                <p class="text-sm font-mono">{timestamp}</p>
            </div>
        </header>
        <div id="stock-cards" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"></div>
    </div>
    <script>
        const stocks = {json.dumps(candidates, ensure_ascii=False)};
        
        function renderCards() {{
            const container = document.getElementById('stock-cards');
            if (!stocks || stocks.length === 0) {{
                container.innerHTML = '<p class="text-center col-span-full text-slate-500">目前無分析數據，請重新執行掃描。</p>';
                return;
            }}
            
            stocks.forEach(stock => {{
                const card = document.createElement('div');
                card.className = 'glass p-6 rounded-2xl shadow-xl';
                
                // Use safe defaults for all variables
                const name = stock.name || '未知個股';
                const sid = stock.id || 'N/A';
                const score = stock.total_score || 0;
                const risk = stock.risk || 'Medium';
                const reasons = stock.reasons || ['無具體理由'];
                const insight = stock.ai_insight || 'AI 分析暫時不可用';
                const component_scores = stock.scores ? Object.values(stock.scores) : [0, 0, 0, 0];

                card.innerHTML = `
                    <div class="flex justify-between items-start mb-4">
                        <div>
                            <h2 class="text-xl font-bold text-white">${{name}} <span class="text-sm font-normal text-slate-400">(${{sid}})</span></h2>
                            <div class="text-3xl font-black text-sky-400 mt-1">${{score}} <span class="text-sm font-normal text-slate-500">/ 100</span></div>
                        </div>
                        <span class="px-3 py-1 rounded-full text-xs font-bold ${{risk === 'Low' ? 'bg-green-900 text-green-400' : 'bg-yellow-900 text-yellow-400'}}">
                            Risk: ${{risk}}
                        </span>
                    </div>
                    <div class="flex justify-center mb-6">
                        <div class="radar-container">
                            <canvas id="chart-${{sid}}"></canvas>
                        </div>
                    </div>
                    <div class="space-y-4">
                        <div>
                            <p class="text-xs text-slate-500 uppercase mb-1">推薦理由</p>
                            <ul class="text-sm text-slate-300 space-y-1">
                                ${{reasons.map(r => `<li>✅ ${{r}}</li>`).join('')}}
                            </ul>
                        </div>
                        <div class="p-3 bg-slate-800 rounded-lg border-l-4 border-sky-500">
                            <p class="text-xs text-sky-400 uppercase font-bold mb-1">🤖 AI 深度洞察</p>
                            <p class="text-sm text-slate-300 italic">${{insight}}</p>
                        </div>
                    </div>
                `;
                container.appendChild(card);
                renderChart(stock);
            }});
        }}

        function renderChart(stock) {{
            const canvas = document.getElementById('chart-' + stock.id);
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            const data = stock.scores ? Object.values(stock.scores) : [0, 0, 0, 0];
            
            new Chart(ctx, {{
                type: 'radar',
                data: {{
                    labels: ['基本面', '技術面', '籌碼面', '消息面'],
                    datasets: [{{
                        label: 'Score',
                        data: data,
                        backgroundColor: 'rgba(56, 189, 248, 0.2)',
                        borderColor: 'rgba(56, 189, 248, 1)',
                        borderWidth: 2,
                        pointBackgroundColor: 'rgba(56, 189, 248, 1)'
                    }}]
                }},
                options: {{
                    scales: {{
                        r: {{
                            angleLines: {{ color: 'rgba(255,255,255,0.1)' }},
                            grid: {{ color: 'rgba(255,255,255,0.1)' }},
                            pointLabels: {{ color: '#94a3b8', font: {{ size: 12 }} }},
                            ticks: {{ display: false }},
                            suggestedMin: 0,
                            suggestedMax: 100
                        }}
                    }},
                    plugins: {{ legend: {{ display: false }} }}
                }}
            }});
        }}
        window.onload = renderCards;
    </script>
</body>
</html>
"""
        # Write to index.html
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("✅ index.html generated with robust template!")

    @staticmethod
    def deploy():
        try:
            repo = Repo(".")
            repo.git.add("index.html")
            repo.index.commit("Automated Dashboard Update")
            origin = repo.remote(name="origin")
            origin.push(refspec="main:main", force=True)
            print("🚀 Deployed to GitHub Pages successfully!")
        except Exception as e:
            print(f"❌ Deploy failed: {e}")
