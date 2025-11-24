import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend
} from "chart.js";
import { Line } from "react-chartjs-2";
import { EmotionPoint } from "../../hooks/useEventAnalysis";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend);

interface Props {
  data: EmotionPoint[];
}

export function EmotionTrendChart({ data }: Props) {
  const labels = data.map((point) => new Date(point.timestamp).toLocaleTimeString());
  const chartData = {
    labels,
    datasets: [
      {
        label: "Positive",
        borderColor: "#22c55e",
        data: data.map((point) => point.positive)
      },
      {
        label: "Neutral",
        borderColor: "#eab308",
        data: data.map((point) => point.neutral)
      },
      {
        label: "Negative",
        borderColor: "#ef4444",
        data: data.map((point) => point.negative)
      }
    ]
  };
  return (
    <div className="rounded-lg border border-slate-700/40 bg-slate-900/40 p-4">
      <h3 className="mb-2 text-sm uppercase tracking-wide text-slate-400">Emotion Trend</h3>
      <Line data={chartData} options={{ responsive: true, plugins: { legend: { position: "bottom" } } }} />
    </div>
  );
}
