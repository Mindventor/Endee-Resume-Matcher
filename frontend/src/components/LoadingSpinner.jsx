export default function LoadingSpinner({ message = 'Analyzing...' }) {
    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
            <div className="glass-card p-8 flex flex-col items-center gap-4 animate-fade-in">
                <div className="relative w-10 h-10">
                    <div className="absolute inset-0 rounded-full border-2 border-zinc-700" />
                    <div
                        className="absolute inset-0 rounded-full border-2 border-transparent border-t-emerald-500"
                        style={{ animation: 'spin 0.8s linear infinite' }}
                    />
                </div>
                <p className="text-sm font-medium text-zinc-400">{message}</p>
                <div className="h-0.5 w-40 rounded-full overflow-hidden bg-zinc-800">
                    <div
                        className="h-full rounded-full bg-emerald-500/60"
                        style={{
                            animation: 'shimmer 1.5s ease-in-out infinite',
                            backgroundSize: '200% 100%',
                            backgroundImage: 'linear-gradient(90deg, transparent, rgba(16,185,129,0.4), transparent)',
                        }}
                    />
                </div>
            </div>
        </div>
    );
}
