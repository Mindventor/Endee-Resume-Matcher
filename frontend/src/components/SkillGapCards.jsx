export default function SkillGapCards({ matchedSkills = [], missingSkills = [], additionalSkills = [] }) {
    const totalRequired = matchedSkills.length + missingSkills.length;
    const coverage = totalRequired > 0 ? Math.round((matchedSkills.length / totalRequired) * 100) : 0;

    return (
        <div className="glass-card p-5 animate-fade-in-up" style={{ animationDelay: '0.05s' }}>
            <div className="flex items-center gap-3 mb-4">
                <div className="w-9 h-9 rounded-lg bg-zinc-800 flex items-center justify-center text-base">🧩</div>
                <div>
                    <h3 className="text-[15px] font-semibold text-zinc-100">Skill Analysis</h3>
                    <p className="text-xs text-zinc-500">
                        {matchedSkills.length} matched · {missingSkills.length} gaps · {additionalSkills.length} bonus
                    </p>
                </div>
            </div>

            <div className="space-y-4">
                {matchedSkills.length > 0 && (
                    <SkillSection
                        label="Matched"
                        count={matchedSkills.length}
                        dotColor="bg-emerald-500"
                        labelColor="text-emerald-400"
                        skills={matchedSkills}
                        chipClass="matched"
                        prefix="✓"
                        showSim
                    />
                )}

                {missingSkills.length > 0 && (
                    <SkillSection
                        label="Missing"
                        count={missingSkills.length}
                        dotColor="bg-red-500"
                        labelColor="text-red-400"
                        skills={missingSkills}
                        chipClass="missing"
                        prefix="✗"
                    />
                )}

                {additionalSkills.length > 0 && (
                    <SkillSection
                        label="Additional"
                        count={additionalSkills.length}
                        dotColor="bg-zinc-500"
                        labelColor="text-zinc-400"
                        skills={additionalSkills}
                        chipClass="additional"
                        prefix="+"
                    />
                )}

                {totalRequired > 0 && (
                    <div className="pt-3 border-t border-white/[0.06]">
                        <div className="flex items-center justify-between text-[11px] mb-1.5">
                            <span className="text-zinc-500">Skill Coverage</span>
                            <span className="font-mono font-medium text-zinc-300">{coverage}%</span>
                        </div>
                        <div className="h-1.5 rounded-full bg-zinc-800 overflow-hidden">
                            <div
                                className="h-full rounded-full bg-emerald-500 transition-all duration-700 ease-out"
                                style={{ width: `${coverage}%` }}
                            />
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

function SkillSection({ label, count, dotColor, labelColor, skills, chipClass, prefix, showSim }) {
    return (
        <div>
            <div className="flex items-center gap-1.5 mb-2">
                <div className={`w-1.5 h-1.5 rounded-full ${dotColor}`} />
                <span className={`text-[11px] font-medium ${labelColor} uppercase tracking-wider`}>
                    {label} ({count})
                </span>
            </div>
            <div className="flex flex-wrap gap-1.5 stagger-children">
                {skills.map((s, i) => (
                    <span key={i} className={`skill-chip ${chipClass}`}>
                        {prefix} {s.skill}
                        {showSim && (
                            <span className="text-[10px] opacity-50 font-mono">
                                {Math.round(s.similarity * 100)}%
                            </span>
                        )}
                    </span>
                ))}
            </div>
        </div>
    );
}
