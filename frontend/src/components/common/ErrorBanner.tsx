interface Props {
  message: string;
}

export function ErrorBanner({ message }: Props) {
  return (
    <div className="rounded-md border border-danger/40 bg-danger/20 px-4 py-3 text-sm text-danger">
      错误：{message}
    </div>
  );
}
