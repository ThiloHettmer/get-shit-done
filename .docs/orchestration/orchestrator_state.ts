import { PhaseInfo, Checkpoint, ExecutorOutput, PlanArtifact, PlanIssue, PlanID } from './component_schemas';

/**
 * GSD Orchestrator State
 * Defines the comprehensive state object used by the LangGraph orchestrator.
 * This state is passed between nodes and persists across the execution lifecycle.
 */

// ============================================================================
// State Interface
// ============================================================================

export interface GSDOrchestratorState {
  // --------------------------------------------------------------------------
  // Static Configuration (Immutable during run)
  // --------------------------------------------------------------------------
  projectRoot: string;
  config: {
    modelProfile: 'speed' | 'balanced' | 'quality';
    parallelization: boolean;
    researchEnabled: boolean;
    planCheckerEnabled: boolean;
    verificationEnabled: boolean;
    maxPlanningIterations: number;
  };
  
  // --------------------------------------------------------------------------
  // Active Scope
  // --------------------------------------------------------------------------
  activePhase: PhaseInfo;
  
  // --------------------------------------------------------------------------
  // Artifact Cache (Loaded from disk, updated by agents)
  // --------------------------------------------------------------------------
  artifacts: {
    roadmap: string;         // Content of ROADMAP.md
    state: string;          // Content of STATE.md
    requirements: string;    // Content of REQUIREMENTS.md
    context?: string;       // Content of CONTEXT.md (User Decisions)
    
    // Phase-specific artifacts
    research?: string;      // Content of [PHASE]-RESEARCH.md
    verification?: string;  // Content of [PHASE]-VERIFICATION.md
    uat?: string;          // Content of [PHASE]-UAT.md
  };

  // --------------------------------------------------------------------------
  // Planning State
  // --------------------------------------------------------------------------
  planning: {
    status: 'pending' | 'in_progress' | 'complete' | 'failed';
    mode: 'standard' | 'gap_closure' | 'revision';
    iteration: number;
    plans: Record<PlanID, PlanArtifact>; // Map of PlanID -> Plan Content
    issues: PlanIssue[]; // Latest checker issues
  };

  // --------------------------------------------------------------------------
  // Execution State
  // --------------------------------------------------------------------------
  execution: {
    status: 'pending' | 'in_progress' | 'paused' | 'complete' | 'failed';
    
    // Wave Management
    waves: Record<number, PlanID[]>; // Map of Wave Number -> List of Plan IDs
    totalWaves: number;
    currentWave: number;
    
    // Plan Status Tracking
    completedPlans: Set<PlanID>;
    failedPlans: Set<PlanID>;
    inProgressPlans: Set<PlanID>;
    
    // Results & Checkpoints
    results: Record<PlanID, ExecutorOutput>;
    activeCheckpoints: Record<PlanID, Checkpoint>; // Plans currently paused at a checkpoint
    
    // Deviations encountered
    deviations: string[];
  };

  // --------------------------------------------------------------------------
  // Global System State
  // --------------------------------------------------------------------------
  // Any global error that stops the entire orchestration
  error?: {
    code: string;
    message: string;
    context?: any;
  };
}

// ============================================================================
// Initial State Factory
// ============================================================================

export function createInitialState(
  projectRoot: string, 
  phase: PhaseInfo,
  config: Partial<GSDOrchestratorState['config']> = {}
): GSDOrchestratorState {
  return {
    projectRoot,
    config: {
      modelProfile: 'balanced',
      parallelization: true,
      researchEnabled: true,
      planCheckerEnabled: true,
      verificationEnabled: true,
      maxPlanningIterations: 3,
      ...config
    },
    activePhase: phase,
    artifacts: {
      roadmap: '',
      state: '',
      requirements: ''
    },
    planning: {
      status: 'pending',
      mode: 'standard',
      iteration: 0,
      plans: {},
      issues: []
    },
    execution: {
      status: 'pending',
      waves: {},
      totalWaves: 0,
      currentWave: 0,
      completedPlans: new Set(),
      failedPlans: new Set(),
      inProgressPlans: new Set(),
      results: {},
      activeCheckpoints: {},
      deviations: []
    }
  };
}
