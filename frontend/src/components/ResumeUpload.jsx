import { useRef, useState } from 'react';

export default function ResumeUpload({ onUpload, isUploading, uploadResult }) {
    const fileInputRef = useRef(null);
    const [isDragging, setIsDragging] = useState(false);
    const [selectedFile, setSelectedFile] = useState(null);

    const handleDrag = (e) => { e.preventDefault(); e.stopPropagation(); };
    const handleDragIn = (e) => { e.preventDefault(); setIsDragging(true); };
    const handleDragOut = (e) => { e.preventDefault(); setIsDragging(false); };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);
        const file = e.dataTransfer.files?.[0];
        if (file) handleFile(file);
    };

    const handleFile = (file) => {
        const ext = file.name.split('.').pop().toLowerCase();
        if (!['pdf', 'docx', 'doc', 'txt'].includes(ext)) {
            alert('Please upload a PDF, DOCX, or TXT file.');
            return;
        }
        if (file.size > 10 * 1024 * 1024) {
            alert('File too large. Maximum size: 10MB.');
            return;
        }
        setSelectedFile(file);
        onUpload(file);
    };

    const handleClick = () => fileInputRef.current?.click();
    const handleChange = (e) => { const file = e.target.files?.[0]; if (file) handleFile(file); };

    return (
        <div className="glass-card p-5 animate-fade-in-up">
            <div className="flex items-center gap-3 mb-4">
                <div className="w-9 h-9 rounded-lg bg-zinc-800 flex items-center justify-center text-base">📄</div>
                <div>
                    <h2 className="text-[15px] font-semibold text-zinc-100">Upload Resume</h2>
                    <p className="text-xs text-zinc-500">PDF, DOCX, or TXT — max 10MB</p>
                </div>
            </div>

            <div
                onClick={handleClick}
                onDragEnter={handleDragIn}
                onDragLeave={handleDragOut}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                className={`
                    relative cursor-pointer rounded-lg border border-dashed p-7
                    flex flex-col items-center justify-center gap-2.5 transition-all duration-200
                    ${isDragging
                        ? 'border-emerald-500/40 bg-emerald-500/[0.04]'
                        : uploadResult
                            ? 'border-emerald-500/20 bg-emerald-500/[0.03]'
                            : 'border-zinc-700 hover:border-zinc-600 hover:bg-white/[0.01]'
                    }
                `}
            >
                <input
                    ref={fileInputRef}
                    type="file"
                    accept=".pdf,.docx,.doc,.txt"
                    onChange={handleChange}
                    className="hidden"
                />

                {isUploading ? (
                    <>
                        <div className="w-8 h-8 rounded-full border-2 border-transparent border-t-emerald-500"
                            style={{ animation: 'spin 0.8s linear infinite' }} />
                        <p className="text-sm text-zinc-400">Processing...</p>
                    </>
                ) : uploadResult ? (
                    <>
                        <div className="w-10 h-10 rounded-full bg-emerald-500/10 flex items-center justify-center text-emerald-400 text-lg">✓</div>
                        <p className="text-sm font-medium text-emerald-400">{selectedFile?.name || 'Resume uploaded'}</p>
                        <p className="text-xs text-zinc-500">{uploadResult.skills?.length || 0} skills extracted</p>
                    </>
                ) : (
                    <>
                        <div className="w-10 h-10 rounded-lg bg-zinc-800 flex items-center justify-center text-xl text-zinc-500">↑</div>
                        <p className="text-sm text-zinc-400">
                            <span className="font-medium text-zinc-300">Click to upload</span> or drag and drop
                        </p>
                    </>
                )}
            </div>

            {uploadResult?.skills?.length > 0 && (
                <div className="mt-4 animate-fade-in">
                    <p className="text-[11px] font-medium text-zinc-500 uppercase tracking-wider mb-2.5">Extracted Skills</p>
                    <div className="flex flex-wrap gap-1.5 stagger-children">
                        {uploadResult.skills.map((skill, i) => (
                            <span key={i} className="skill-chip additional">{skill}</span>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
