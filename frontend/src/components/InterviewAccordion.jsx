import { useState } from 'react';

export default function InterviewAccordion({ questions = [] }) {
    const [openIndex, setOpenIndex] = useState(null);
    const toggle = (i) => setOpenIndex(openIndex === i ? null : i);

    if (!questions.length) return null;

    return (
        <div className="glass-card p-5 animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
            <div className="flex items-center gap-3 mb-4">
                <div className="w-9 h-9 rounded-lg bg-zinc-800 flex items-center justify-center text-base">💡</div>
                <div>
                    <h3 className="text-[15px] font-semibold text-zinc-100">Interview Questions</h3>
                    <p className="text-xs text-zinc-500">
                        {questions.length} questions · Retrieved via Endee RAG
                    </p>
                </div>
            </div>

            <div className="space-y-1 stagger-children">
                {questions.map((q, i) => {
                    const isOpen = openIndex === i;
                    return (
                        <div key={i} className="border border-white/[0.04] rounded-lg overflow-hidden transition-colors hover:border-white/[0.08]">
                            <button
                                onClick={() => toggle(i)}
                                className="w-full flex items-start gap-2.5 p-3.5 text-left transition-colors hover:bg-white/[0.015]"
                            >
                                <span className="text-[11px] font-mono text-zinc-600 mt-0.5 shrink-0 w-5">
                                    {String(i + 1).padStart(2, '0')}
                                </span>

                                <div className="flex-1 min-w-0">
                                    <p className="text-sm text-zinc-300 leading-relaxed pr-2">{q.question}</p>
                                    <div className="flex items-center gap-1.5 mt-2">
                                        <Badge label={q.category} />
                                        <DifficultyBadge difficulty={q.difficulty} />
                                        <span className="text-[10px] text-zinc-600 font-mono ml-auto">
                                            {Math.round(q.relevance_score * 100)}%
                                        </span>
                                    </div>
                                </div>

                                <svg
                                    className={`w-4 h-4 text-zinc-600 shrink-0 mt-0.5 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`}
                                    fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2"
                                >
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
                                </svg>
                            </button>

                            {isOpen && (
                                <div className="px-3.5 pb-3.5 animate-fade-in">
                                    <div className="ml-7 pl-3 border-l border-zinc-800">
                                        <p className="text-[10px] font-medium text-zinc-500 uppercase tracking-wider mb-1.5">
                                            Key Points
                                        </p>
                                        <ul className="space-y-1">
                                            {q.key_points.map((point, j) => (
                                                <li key={j} className="flex items-start gap-1.5 text-[13px] text-zinc-400">
                                                    <span className="text-zinc-600 mt-px text-[10px]">—</span>
                                                    {point}
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
}

function Badge({ label }) {
    return (
        <span className="text-[10px] font-medium px-2 py-0.5 rounded bg-zinc-800 text-zinc-400 border border-white/[0.04]">
            {label}
        </span>
    );
}

function DifficultyBadge({ difficulty }) {
    const colors = {
        Easy: 'text-emerald-400',
        Medium: 'text-yellow-400',
        Hard: 'text-red-400',
    };
    return (
        <span className={`text-[10px] font-medium px-2 py-0.5 rounded bg-zinc-800 border border-white/[0.04] ${colors[difficulty] || 'text-zinc-400'}`}>
            {difficulty}
        </span>
    );
}
