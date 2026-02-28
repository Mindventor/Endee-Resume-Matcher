import { useState } from 'react';

export default function JobDescription({ onAnalyze, isAnalyzing, disabled }) {
    const [text, setText] = useState('');

    const handleSubmit = () => {
        if (text.trim().length < 10) return;
        onAnalyze(text.trim());
    };

    const isDisabled = disabled || isAnalyzing || text.trim().length < 10;

    return (
        <div className="glass-card p-5 animate-fade-in-up" style={{ animationDelay: '0.05s' }}>
            <div className="flex items-center gap-3 mb-4">
                <div className="w-9 h-9 rounded-lg bg-zinc-800 flex items-center justify-center text-base">🎯</div>
                <div>
                    <h2 className="text-[15px] font-semibold text-zinc-100">Job Description</h2>
                    <p className="text-xs text-zinc-500">Paste the target role description</p>
                </div>
            </div>

            <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Paste the job description here..."
                rows={6}
                className="w-full bg-zinc-900/50 border border-zinc-800 rounded-lg px-3.5 py-2.5 text-sm text-zinc-200 placeholder-zinc-600 resize-none focus:outline-none focus:border-zinc-600 transition-colors duration-150"
            />

            <div className="flex items-center justify-between mt-3">
                <span className="text-[11px] text-zinc-600 font-mono">{text.length} chars</span>
                <button
                    onClick={handleSubmit}
                    disabled={isDisabled}
                    className={`
                        px-5 py-2 rounded-lg text-sm font-medium transition-all duration-150
                        ${isDisabled
                            ? 'bg-zinc-800 text-zinc-600 cursor-not-allowed'
                            : 'bg-emerald-500 text-white hover:bg-emerald-400 active:bg-emerald-600'
                        }
                    `}
                >
                    {isAnalyzing ? (
                        <span className="flex items-center gap-2">
                            <span className="w-3.5 h-3.5 rounded-full border-2 border-transparent border-t-white"
                                style={{ animation: 'spin 0.8s linear infinite' }} />
                            Analyzing...
                        </span>
                    ) : (
                        'Analyze Match'
                    )}
                </button>
            </div>
        </div>
    );
}
