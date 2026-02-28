export default function Layout({ children }) {
    return (
        <div className="min-h-screen bg-grid">
            {/* ── Sidebar ────────────────────────────────────────────────── */}
            <aside className="fixed left-0 top-0 bottom-0 w-60 border-r border-white/[0.06] bg-zinc-950/80 backdrop-blur-md z-40 flex flex-col max-lg:hidden">
                {/* Logo */}
                <div className="px-5 py-5 border-b border-white/[0.06]">
                    <div className="flex items-center gap-2.5">
                        <div className="w-8 h-8 rounded-lg bg-emerald-500 flex items-center justify-center text-sm font-bold text-white">
                            E
                        </div>
                        <div>
                            <h1 className="text-sm font-semibold text-zinc-100 tracking-tight">Endee</h1>
                            <p className="text-[10px] text-zinc-500 font-medium">Resume Intelligence</p>
                        </div>
                    </div>
                </div>

                {/* Nav */}
                <nav className="flex-1 px-3 py-3 space-y-0.5">
                    <NavItem icon="📊" label="Home" active />
                </nav>

                {/* Footer */}
                <div className="px-4 py-4 border-t border-white/[0.06]">
                    <p className="text-[10px] text-zinc-600">Powered by Endee Vector DB</p>
                </div>
            </aside>

            {/* ── Mobile Header ──────────────────────────────────────────── */}
            <header className="lg:hidden fixed top-0 left-0 right-0 h-13 border-b border-white/[0.06] bg-zinc-950/90 backdrop-blur-md z-40 flex items-center px-4">
                <div className="flex items-center gap-2">
                    <div className="w-7 h-7 rounded-md bg-emerald-500 flex items-center justify-center text-xs font-bold text-white">
                        E
                    </div>
                    <span className="text-sm font-semibold text-zinc-100">Endee</span>
                </div>
            </header>

            {/* ── Main Content ───────────────────────────────────────────── */}
            <main className="lg:ml-60 min-h-screen">
                <div className="max-w-5xl mx-auto px-5 py-6 lg:px-8 lg:py-8 max-lg:pt-18">
                    {children}
                </div>
            </main>
        </div>
    );
}

function NavItem({ icon, label, active = false }) {
    return (
        <button
            className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-[13px] font-medium transition-colors duration-150 ${active
                ? 'bg-white/[0.06] text-zinc-100'
                : 'text-zinc-500 hover:text-zinc-300 hover:bg-white/[0.03]'
                }`}
        >
            <span className="text-sm">{icon}</span>
            {label}
        </button>
    );
}
