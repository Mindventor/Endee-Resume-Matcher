import { useState } from 'react';
import ResumeUpload from '../components/ResumeUpload';
import JobDescription from '../components/JobDescription';
import MatchScore from '../components/MatchScore';
import SkillGapCards from '../components/SkillGapCards';
import InterviewAccordion from '../components/InterviewAccordion';
import LearningCards from '../components/LearningCards';
import LoadingSpinner from '../components/LoadingSpinner';
import { uploadResume, analyzeMatch } from '../api/client';

export default function Dashboard() {
    const [uploadResult, setUploadResult] = useState(null);
    const [analysisResult, setAnalysisResult] = useState(null);
    const [isUploading, setIsUploading] = useState(false);
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [error, setError] = useState(null);

    const handleUpload = async (file) => {
        setIsUploading(true);
        setError(null);
        setAnalysisResult(null);
        try {
            const res = await uploadResume(file);
            setUploadResult(res.data);
        } catch (err) {
            setError(err.response?.data?.detail || err.message || 'Upload failed');
        } finally {
            setIsUploading(false);
        }
    };

    const handleAnalyze = async (jobDescription) => {
        if (!uploadResult?.extracted_text) {
            setError('Please upload a resume first.');
            return;
        }
        setIsAnalyzing(true);
        setError(null);
        try {
            const res = await analyzeMatch(uploadResult.extracted_text, jobDescription);
            setAnalysisResult(res.data);
        } catch (err) {
            setError(err.response?.data?.detail || err.message || 'Analysis failed');
        } finally {
            setIsAnalyzing(false);
        }
    };

    return (
        <div>
            {isAnalyzing && <LoadingSpinner message="Running analysis..." />}

            {/* Header */}
            <div className="mb-7 animate-fade-in-up">
                <h1 className="text-2xl font-bold text-zinc-100 tracking-tight">
                    Resume Intelligence
                </h1>
                <p className="text-sm text-zinc-500 mt-1 max-w-lg">
                    Upload your resume and a job description to get match scoring,
                    skill gap analysis, interview questions, and learning recommendations.
                </p>
            </div>

            {/* Error */}
            {error && (
                <div className="mb-5 p-3.5 rounded-lg border border-red-500/15 bg-red-500/[0.06] flex items-center gap-2.5 animate-fade-in">
                    <span className="text-red-400 text-sm">⚠</span>
                    <p className="text-sm text-red-300/80 flex-1">{error}</p>
                    <button onClick={() => setError(null)} className="text-red-400/60 hover:text-red-300 text-sm">✕</button>
                </div>
            )}

            {/* Input */}
            <div className="grid gap-4 lg:grid-cols-2 mb-7">
                <ResumeUpload onUpload={handleUpload} isUploading={isUploading} uploadResult={uploadResult} />
                <JobDescription onAnalyze={handleAnalyze} isAnalyzing={isAnalyzing} disabled={!uploadResult} />
            </div>

            {/* Results */}
            {analysisResult && (
                <div className="space-y-4">
                    {/* Summary */}
                    <div className="glass-card p-4 animate-fade-in-up">
                        <p className="text-sm text-zinc-400 leading-relaxed">
                            <span className="font-medium text-zinc-300">Summary — </span>
                            {analysisResult.summary}
                        </p>
                    </div>

                    {/* Score + Skills */}
                    <div className="grid gap-4 lg:grid-cols-[260px_1fr]">
                        <MatchScore score={analysisResult.match_score} label={analysisResult.match_label} />
                        <SkillGapCards
                            matchedSkills={analysisResult.matched_skills}
                            missingSkills={analysisResult.missing_skills}
                            additionalSkills={analysisResult.additional_skills}
                        />
                    </div>

                    <InterviewAccordion questions={analysisResult.interview_questions} />
                    <LearningCards resources={analysisResult.learning_resources} />
                </div>
            )}

            {/* Empty state */}
            {!analysisResult && !isAnalyzing && (
                <div className="mt-16 text-center animate-fade-in">
                    <p className="text-zinc-600 text-sm">
                        Upload a resume and enter a job description to begin analysis.
                    </p>
                </div>
            )}
        </div>
    );
}
