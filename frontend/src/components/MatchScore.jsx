import { useEffect, useState } from 'react';

export default function MatchScore({ score, label }) {
    const [animatedScore, setAnimatedScore] = useState(0);
    const radius = 72;
    const circumference = 2 * Math.PI * radius;
    const progress = (animatedScore / 100) * circumference;
    const offset = circumference - progress;

    const getColor = (s) => {
        if (s >= 75) return '#10b981';
        if (s >= 55) return '#eab308';
        if (s >= 35) return '#f97316';
        return '#ef4444';
    };

    const color = getColor(score);

    useEffect(() => {
        let start = 0;
        const end = score;
        const duration = 1200;
        const stepTime = 16;
        const steps = duration / stepTime;
        const increment = end / steps;

        const timer = setInterval(() => {
            start += increment;
            if (start >= end) {
                setAnimatedScore(end);
                clearInterval(timer);
            } else {
                setAnimatedScore(Math.round(start * 10) / 10);
            }
        }, stepTime);

        return () => clearInterval(timer);
    }, [score]);

    return (
        <div className="glass-card p-6 flex flex-col items-center animate-fade-in-up">
            <h3 className="text-[11px] font-medium text-zinc-500 uppercase tracking-wider mb-5">Match Score</h3>

            <div className="relative w-44 h-44">
                <svg className="w-full h-full -rotate-90" viewBox="0 0 180 180">
                    {/* Background ring */}
                    <circle cx="90" cy="90" r={radius} fill="none" stroke="rgba(255,255,255,0.04)" strokeWidth="8" />
                    {/* Progress arc */}
                    <circle
                        cx="90" cy="90" r={radius} fill="none"
                        stroke={color}
                        strokeWidth="8"
                        strokeLinecap="round"
                        strokeDasharray={circumference}
                        strokeDashoffset={offset}
                        style={{ transition: 'stroke-dashoffset 0.2s ease' }}
                    />
                </svg>

                <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span
                        className="text-4xl font-bold"
                        style={{ fontFamily: 'var(--font-mono)', color }}
                    >
                        {Math.round(animatedScore)}
                    </span>
                    <span className="text-[11px] text-zinc-600 mt-0.5">/ 100</span>
                </div>
            </div>

            <div
                className="mt-5 px-3.5 py-1.5 rounded-md text-xs font-medium"
                style={{ background: `${color}10`, color }}
            >
                {label}
            </div>
        </div>
    );
}
