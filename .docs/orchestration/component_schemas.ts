/**
 * GSD Component Schemas
 * Defines the interfaces for the autonomous agents and the orchestration state.
 */

// ============================================================================
// Shared Domain Types
// ============================================================================

export type PhaseNumber = string; // "01", "02.1"
export type PlanID = string; // "01-01", "02-03"

export interface PhaseInfo {
  number: PhaseNumber;
  name: string;
  directory: string;
  goal: string;
}

export interface VerificationResult {
  status: 'passed' | 'human_needed' | 'gaps_found';
  gaps?: string[];
  humanVerificationSteps?: string[];
}

export interface Checkpoint {
  type: 'human-verify' | 'decision' | 'human-action';
  planId: PlanID;
  taskNumber: number;
  description: string;
  awaiting: string;
  options?: Array<{ id: string; name: string; description: string }>;
}

// ============================================================================
// Autonomous Component Interfaces
// ============================================================================

/**
 * 1. Phase Researcher
 * Gathers context to inform planning.
 */
export interface ResearcherInput {
  phase: PhaseInfo;
  requirements: string; // Content of REQUIREMENTS.md
  roadmapContext: string; // Relevant section from ROADMAP.md
  userDecisions?: string; // Content of CONTEXT.md
  currentState: string; // Content of STATE.md
}

export interface ResearcherOutput {
  researchContent: string; // Content for [PHASE]-RESEARCH.md
  blocked: boolean;
  blockerReason?: string;
}

/**
 * 2. Planner
 * Decomposes phase goal into executable plans.
 */
export interface PlannerInput {
  mode: 'standard' | 'gap_closure' | 'revision';
  phase: PhaseInfo;
  projectState: string;
  roadmap: string;
  requirements: string;
  context?: string; // User decisions
  research: string; // Research output
  verificationGaps?: string; // Only for gap_closure mode
  existingPlans?: Record<PlanID, string>; // For revision mode
  checkerIssues?: any[]; // For revision mode
}

export interface PlanArtifact {
  id: PlanID;
  filename: string;
  content: string; // The markdown content of the plan
  frontmatter: {
    wave: number;
    autonomous: boolean;
    files_modified: string[];
    depends_on: PlanID[];
  };
}

export interface PlannerOutput {
  plans: PlanArtifact[];
  status: 'complete' | 'inconclusive';
}

/**
 * 3. Plan Checker (Verifier)
 * Validates generated plans.
 */
export interface PlanCheckerInput {
  phase: PhaseInfo;
  plans: PlanArtifact[];
  requirements: string;
  userDecisions?: string;
}

export interface PlanIssue {
  planId: PlanID;
  severity: 'blocker' | 'warning';
  dimension: 'completeness' | 'compliance' | 'dependencies';
  description: string;
  fixHint?: string;
}

export interface PlanCheckerOutput {
  status: 'passed' | 'issues_found';
  issues: PlanIssue[];
}

/**
 * 4. Executor
 * Executes a single plan.
 */
export interface ExecutorInput {
  plan: PlanArtifact;
  projectState: string;
  config: any; // Project config
}

export interface ExecutorOutput {
  summary: string; // Content of SUMMARY.md
  commits: Array<{ hash: string; message: string }>;
  checkpoint?: Checkpoint; // If execution paused
  deviations: string[];
  status: 'complete' | 'paused' | 'failed';
}

/**
 * 5. Phase Verifier
 * Verifies phase goal achievement.
 */
export interface PhaseVerifierInput {
  phase: PhaseInfo;
  phaseDir: string;
  mustHaves: any[]; // Derived from planning
}

export interface PhaseVerifierOutput {
  status: 'passed' | 'human_needed' | 'gaps_found';
  verificationContent: string; // Content for VERIFICATION.md
}

// ============================================================================
// Orchestration State
// ============================================================================

/**
 * Central state object for LangGraph orchestration.
 * Persists across the graph execution.
 */
export interface GSDOrchestratorState {
  // Static Context
  projectRoot: string;
  config: {
    modelProfile: string;
    parallelization: boolean;
    researchEnabled: boolean;
    verificationEnabled: boolean;
  };

  // Active Scope
  activePhase: PhaseInfo;

  // Artifact Cache (loaded from disk)
  artifacts: {
    roadmap: string;
    state: string;
    requirements: string;
    context?: string;
    research?: string;
    verification?: string;
  };

  // Execution Tracking
  planning: {
    iteration: number;
    plans: Record<PlanID, PlanArtifact>;
    issues: PlanIssue[];
  };
  
  execution: {
    waves: Record<number, PlanID[]>; // Wave sets
    currentWave: number;
    completedPlans: Set<PlanID>;
    pendingPlans: Set<PlanID>;
    activeCheckpoints: Record<PlanID, Checkpoint>;
    results: Record<PlanID, ExecutorOutput>;
  };
}
