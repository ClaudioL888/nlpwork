interface Props {
  label?: string;
}

export function LoadingState({ label = "加载中" }: Props) {
  return (
    <div className="flex items-center gap-3 text-slate-300 animate-pulse">
      <span className="h-3 w-3 rounded-full bg-primary animate-bounce" />
      <span>{label}...</span>
    </div>
  );
}
