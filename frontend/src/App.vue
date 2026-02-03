<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const API_URL = 'http://localhost:8000/api';
const operadoras = ref([]);
const stats = ref({ total_geral: 0, media_nacional: 0, top_5: [], total_ops: 0 });
const search = ref('');
const page = ref(1);
const loading = ref(false);

const formatCurrency = (val) => new Intl.NumberFormat('pt-BR', { 
  style: 'currency', currency: 'BRL', maximumFractionDigits: 0 
}).format(val || 0);

const fetchData = async () => {
  loading.value = true;
  try {
    const res = await axios.get(`${API_URL}/operadoras`, { 
      params: { page: page.value, search: search.value } 
    });
    // Agora acessando 'data' vindo do backend
    operadoras.value = res.data.data;
  } catch (e) { 
    console.error("Erro ao carregar operadoras", e); 
  } finally { 
    loading.value = false; 
  }
};

const fetchStats = async () => {
  try {
    const res = await axios.get(`${API_URL}/estatisticas`);
    stats.value = res.data;
  } catch (e) { 
    console.error("Erro ao carregar estatísticas", e); 
  }
};

const chartData = computed(() => ({
  // Ajustado para RAZAO_SOCIAL e VALOR (Maiúsculos)
  labels: stats.value.top_5 ? stats.value.top_5.map(s => s.RAZAO_SOCIAL.substring(0, 15) + '...') : [],
  datasets: [{ 
    label: 'Gasto Total', 
    data: stats.value.top_5 ? stats.value.top_5.map(s => s.VALOR) : [], 
    backgroundColor: '#6366f1',
    borderRadius: 6
  }]
}));

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: { grid: { color: '#334155' }, ticks: { color: '#94a3b8' } },
    x: { ticks: { color: '#94a3b8' } }
  },
  plugins: { legend: { display: false } }
};

onMounted(() => { 
  fetchData(); 
  fetchStats(); 
});
</script>

<template>
  <div class="app-shell">
    <aside class="sidebar">
      <div class="brand"> ANS<span>Data</span></div>
      <nav>
        <div class="nav-item active"> Dashboard Geral</div>
      </nav>
      <div class="sidebar-footer">v1.1.0 - Produção</div>
    </aside>

    <main class="main-content">
      <header class="top-bar">
        <h1>Monitoramento Financeiro</h1>
        <p class="subtitle">Análise de despesas hospitalares e administrativas</p>
      </header>

      <div class="kpi-container">
        <div class="kpi-card">
          <span class="label">Volume Total (3T)</span>
          <div class="value">{{ formatCurrency(stats.total_geral) }}</div>
        </div>
        <div class="kpi-card">
          <span class="label">Média por Operadora</span>
          <div class="value">{{ formatCurrency(stats.media_nacional) }}</div>
        </div>
        <div class="kpi-card">
          <span class="label">Total de Empresas</span>
          <div class="value">{{ stats.total_ops }}</div>
        </div>
      </div>

      <div class="data-grid">
        <div class="glass-panel">
          <div class="panel-header">Maiores Despesas (Top 5)</div>
          <div class="chart-wrapper">
            <Bar :data="chartData" :options="chartOptions" />
          </div>
        </div>

        <div class="glass-panel">
          <div class="panel-header search-header">
            <span>Listagem Detalhada</span>
            <input 
              v-model="search" 
              @input="page=1; fetchData()" 
              placeholder="CNPJ ou Nome da Operadora..." 
            />
          </div>
          
          <div class="table-wrapper" :class="{ 'is-loading': loading }">
            <table>
              <thead>
                <tr>
                  <th>Operadora / UF</th>
                  <th class="text-right">Despesa Acumulada</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="op in operadoras" :key="op.CNPJ">
                  <td>
                    <div class="op-main">{{ op.RAZAO_SOCIAL }}</div>
                    <div class="op-sub">{{ op.CNPJ }} • {{ op.UF }}</div>
                  </td>
                  <td class="text-right">
                    <span class="badge">{{ formatCurrency(op.VALOR) }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="footer-pagination">
            <button @click="page--; fetchData()" :disabled="page <= 1">Anterior</button>
            <span class="page-indicator">Página {{ page }}</span>
            <button @click="page++; fetchData()" :disabled="operadoras.length < 10">Próxima</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.app-shell { display: flex; min-height: 100vh; background: #0f172a; color: #f8fafc; font-family: 'Inter', sans-serif; }
.sidebar { width: 240px; background: #1e293b; border-right: 1px solid #334155; padding: 2rem 1rem; display: flex; flex-direction: column; }
.brand { font-size: 1.5rem; font-weight: 800; margin-bottom: 2.5rem; padding-left: 1rem; }
.brand span { color: #6366f1; }
.nav-item { padding: 0.85rem 1rem; border-radius: 0.5rem; background: #6366f1; color: white; font-weight: 600; font-size: 0.9rem; }
.sidebar-footer { margin-top: auto; font-size: 0.7rem; color: #475569; text-align: center; }
.main-content { flex: 1; padding: 2rem 3rem; overflow-y: auto; }
.top-bar { margin-bottom: 2.5rem; }
.top-bar h1 { font-size: 1.8rem; font-weight: 800; }
.subtitle { color: #94a3b8; font-size: 0.9rem; }
.kpi-container { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin-bottom: 2.5rem; }
.kpi-card { background: #1e293b; padding: 1.5rem; border-radius: 1rem; border: 1px solid #334155; }
.kpi-card .label { color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; }
.kpi-card .value { font-size: 1.6rem; font-weight: 800; margin-top: 0.5rem; }
.data-grid { display: grid; grid-template-columns: 1fr 1.5fr; gap: 2rem; }
.glass-panel { background: #1e293b; border-radius: 1rem; border: 1px solid #334155; padding: 1.5rem; }
.panel-header { font-weight: 700; margin-bottom: 1.5rem; font-size: 1rem; color: #cbd5e1; }
.chart-wrapper { height: 350px; }
.search-header { display: flex; justify-content: space-between; align-items: center; }
.search-header input { background: #0f172a; border: 1px solid #334155; color: white; padding: 0.6rem 1rem; border-radius: 0.6rem; width: 60%; font-size: 0.85rem; outline: none; }
.table-wrapper { min-height: 420px; }
.is-loading { opacity: 0.3; }
table { width: 100%; border-collapse: collapse; }
th { text-align: left; color: #64748b; font-size: 0.7rem; text-transform: uppercase; padding: 1rem; border-bottom: 1px solid #334155; }
td { padding: 1rem; border-bottom: 1px solid #0f172a; }
.op-main { font-weight: 600; font-size: 0.85rem; max-width: 250px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.op-sub { color: #64748b; font-size: 0.7rem; margin-top: 4px; }
.badge { background: rgba(99, 102, 241, 0.1); padding: 0.4rem 0.8rem; border-radius: 0.5rem; font-weight: 700; color: #818cf8; border: 1px solid rgba(99, 102, 241, 0.2); }
.text-right { text-align: right; }
.footer-pagination { display: flex; justify-content: space-between; align-items: center; padding-top: 1.5rem; }
.footer-pagination button { background: #334155; border: none; color: white; padding: 0.5rem 1.2rem; border-radius: 0.5rem; cursor: pointer; font-size: 0.8rem; }
.footer-pagination button:disabled { opacity: 0.2; cursor: not-allowed; }
</style>