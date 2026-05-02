import os
import json
from datetime import datetime
from git import Repo

class DashboardGenerator:
    @staticmethod
    def generate(candidates, market_trend="Bullish"):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        template = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenStock AI | 量化選股儀表板</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: 'Inter', system-ui, sans-serif; }
        .glass { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.1); transition: all 0.3s ease; }
        .glass:hover { border-color: rgba(56, 189, 248, 0.4); transform: translateY(-4px); }
        .chart-box { position: relative; height: 240px; width: 240px; margin: 0 auto; }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-6xl mx-auto">
        <header class="flex flex-col md:flex-row justify-between items-start md:items-center mb-12 gap-4">
            <div>
                <h1 class="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-indigo-500">OpenStock AI</h1>
                <p class="text-slate-400 mt-2 text-lg">量化選股分析報告 | 市場狀態: <span class="text-green-400 font-bold">{{MARKET_TREND}}</span></p>
            </div>
            <div class="bg-slate-800/50 px-4 py-2 rounded-lg border border-slate-700 text-right">
                <p class="text-xs text-slate-500 uppercase font-bold">Last Update</p>
                <p class="text-sm font-mono text-slate-300">{{TIMESTAMP}}</p>
            </div>
        </header>
        <div id="stock-cards" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"></div>
    </div>
    <script>
        const stocks = {{STOCK_DATA}};
        
        function renderCards() {
            const container = document.getElementById('stock-cards');
            if (!stocks || stocks.length === 0) {
                container.innerHTML = '<div class="col-span-full text-center py-20"><p class="text-slate-500 text-xl">目前無符合條件的分析數據</p></div>';
                return;
            }
            
            stocks.forEach(stock => {
                const card = document.createElement('div');
                card.className = 'glass p-6 rounded-3xl shadow-2xl flex flex-col';
                
                const name = stock.name || '未知個股';
                const sid = stock.id || 'NA';
                const score = stock.total_score || 0;
                const risk = stock.risk || 'Medium';
                const reasons = stock.reasons || ['無具體理由'];
                const insight = stock.ai_insight || 'AI 分析暫時不可用';
                
                card.innerHTML = `
                    <div class="flex justify-between items-start mb-6">
                        <div>
                            <h2 class="text-2xl font-bold text-white">${name} <span class="text-sm font-normal text-slate-400">(${sid})</span></h2>
                            <div class="text-4xl font-black text-sky-400 mt-2">${score} <span class="text-sm font-normal text-slate-500">/ 100</span></div>
                        </div>
                        <span class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${risk === 'Low' ? 'bg-green-500/20 text-green-400' : 'bg-yellow-500/20 text-yellow-400'}">
                            ${risk} Risk
                        </span>
                    </div>
                    <div class="chart-box mb-8">
                        <canvas id="stock-chart-${sid}"></canvas>
                    </div>
                    <div class="space-y-6 mt-auto">
                        <div>
                            <p class="text-xs text-slate-500 uppercase font-bold mb-2 tracking-widest">推薦理由</p>
                            <ul class="text-sm text-slate-300 space-y-2">
                                ${reasons.map(r => `<li class="flex items-start"><span class="text-sky-400 mr-2">✦</span> ${r}</li>`).join('')}
                            </ul>
                        </div>
                        <div class="p-4 bg-slate-900/50 rounded-2xl border-l-4 border-sky-500">
                            <p class="text-xs text-sky-400 uppercase font-bold mb-1">🤖 AI 深度洞察</p>
                            <p class="text-sm text-slate-300 leading-relaxed italic">"${insight}"</p>
                        </div>
                    </div>
                `;
                container.appendChild(card);
                renderChart(stock);
            });
        }

        function renderChart(stock) {
            try {
                const canvas = document.getElementById('stock-chart-' + stock.id);
                if (!canvas) return;
                const ctx = canvas.getContext('2d');
                const s = stock.scores || {};
                
                const cleanValue = (val) => {
                    if (val === null || val === undefined) return 0;
                    const parsed = parseFloat(val);
                    return isNaN(parsed) ? 0 : parsed;
                };

                const data = [
                    cleanValue(s.fundamental),
                    cleanValue(s.technical),
                    cleanValue(s.chip),
                    cleanValue(s.ai)
                ];
                
                new Chart(ctx, {
                    type: 'radar',
                    data: {
                        labels: ['基本面', '技術面', '籌碼面', '消息面'],
                        datasets: [{
                            label: 'Score',
                            data: data,
                            backgroundColor: 'rgba(56, 189, 248, 0.4)',
                            borderColor: 'rgba(56, 189, 248, 1)',
                            borderWidth: 4,
                            pointBackgroundColor: 'rgba(56, 189, 248, 1)',
                            pointBorderColor: '#fff',
                            pointRadius: 4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            r: {
                                angleLines: { color: 'rgba(255,255,255,0.1)' },
                                grid: { color: 'rgba(255,255,255,0.1)' },
                                pointLabels: { 
                                    color: '#94a3b8', 
                                    font: { size: 12, weight: 'bold' } 
                                },
                                ticks: { display: false },
                                suggestedMin: 0,
                                suggestedMax: 100
                            }
                        },
                        plugins: { legend: { display: false } }
                    }
                });
            } catch (e) {
                console.error('Critical Chart Error:', e);
            }
        }
        window.onload = renderCards;
    </script>
</body>
</html>
"""
        content = template.replace("{{MARKET_TREND}}", market_trend)
        content = content.replace("{{TIMESTAMP}}", timestamp)
        content = content.replace("{{STOCK_DATA}}", json.dumps(candidates, ensure_ascii=False))
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def deploy():
        try:
            repo = Repo(".")
            repo.git.add("index.html")
            repo.index.commit("Critical Fix: Time-Correction & Strict Cleaning")
            origin = repo.remote(name="origin")
            origin.push(refspec="main:main", force=True)
            print("🚀 Deployed Critical Fix to GitHub Pages!")
        except Exception as e:
            print(f"❌ Deploy failed: {e}")

