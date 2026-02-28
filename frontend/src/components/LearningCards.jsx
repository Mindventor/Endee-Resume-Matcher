export default function LearningCards({ resources = [] }) {
    if (!resources.length) return null;

    const typeIcon = { course: '🎓', tutorial: '📖', documentation: '📄', book: '📚' };

    return (
        <div className="glass-card p-5 animate-fade-in-up" style={{ animationDelay: '0.15s' }}>
            <div className="flex items-center gap-3 mb-4">
                <div className="w-9 h-9 rounded-lg bg-zinc-800 flex items-center justify-center text-base">📚</div>
                <div>
                    <h3 className="text-[15px] font-semibold text-zinc-100">Learning Resources</h3>
                    <p className="text-xs text-zinc-500">{resources.length} resources for your skill gaps</p>
                </div>
            </div>

            <div className="grid gap-2 sm:grid-cols-2 stagger-children">
                {resources.map((r, i) => {
                    const icon = typeIcon[r.resource_type] || '📦';
                    return (
                        <a
                            key={i}
                            href={r.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="group flex items-start gap-2.5 border border-white/[0.04] rounded-lg p-3.5 transition-all duration-150 hover:border-white/[0.08] hover:bg-white/[0.015]"
                        >
                            <span className="text-lg shrink-0">{icon}</span>
                            <div className="flex-1 min-w-0">
                                <h4 className="text-[13px] font-medium text-zinc-300 group-hover:text-zinc-100 transition-colors line-clamp-2 leading-snug">
                                    {r.title}
                                </h4>
                                <p className="text-[11px] text-zinc-600 mt-1">{r.provider}</p>
                                <div className="flex items-center gap-1.5 mt-2">
                                    <span className="text-[10px] font-medium px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-400 border border-white/[0.04]">
                                        {r.resource_type}
                                    </span>
                                    <span className="text-[10px] font-medium px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-500 border border-white/[0.04]">
                                        {r.skill_area}
                                    </span>
                                    <span className="text-[10px] text-zinc-600 font-mono ml-auto">
                                        {Math.round(r.relevance_score * 100)}%
                                    </span>
                                </div>
                            </div>
                            <svg className="w-3.5 h-3.5 text-zinc-700 group-hover:text-zinc-400 transition-colors shrink-0 mt-0.5"
                                fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                            </svg>
                        </a>
                    );
                })}
            </div>
        </div>
    );
}
