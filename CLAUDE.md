# Claude Code Management Guide

This document provides comprehensive guidelines for managing the LegalTech MVP codebase, covering code management workflows, coding approaches, and debugging strategies.

---

# General Note:
Always refer to the documentations like Readme and docs/ before advising


# 1. CODE MANAGEMENT

## 🔄 End-to-End Workflow: Document → Code → Deploy

### Phase 1: Documentation & Planning First

**1.1 Issue Analysis & Architecture Review**
```bash
# Before writing any code:
# 1. Review GitHub issue and requirements
# 2. Study existing architecture docs
# 3. Document implementation approach
# 4. Plan code structure and interfaces
```

**1.2 Document Your Approach**
Create documentation BEFORE coding:
- Update `docs/architecture/` if system design changes
- Plan API changes in `docs/api/` 
- Document new features in `docs/features/`
- Update README.md if setup/commands change

**1.3 Branch Creation**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/ISSUE-123-short-description
```

**Branch Naming Conventions:**
- `feature/ISSUE-123-user-authentication` - New features
- `bugfix/ISSUE-456-fix-login-error` - Bug fixes
- `hotfix/ISSUE-789-critical-security` - Critical production fixes
- `docs/update-api-documentation` - Documentation updates
- `refactor/cleanup-auth-service` - Code improvements

### Phase 2: Code Implementation

**2.1 Code Documentation Standards**

**Inline Code Comments:**
```typescript
/**
 * Authenticates user and returns JWT token
 * @param email - User's email address
 * @param password - Plain text password (will be hashed)
 * @returns Promise<AuthResult> - Contains token and user data
 * @throws AuthenticationError - When credentials are invalid
 * 
 * @example
 * ```typescript
 * const result = await authenticateUser('user@example.com', 'password123');
 * console.log(result.token); // JWT token
 * ```
 */
export async function authenticateUser(email: string, password: string): Promise<AuthResult> {
  // Hash the password using bcrypt with salt rounds from config
  const hashedPassword = await bcrypt.hash(password, config.SALT_ROUNDS);
  
  // Query database for user - using email index for performance
  const user = await User.findOne({ email });
  if (!user) {
    throw new AuthenticationError('Invalid credentials');
  }
  
  // Compare passwords and generate JWT if valid
  const isValid = await bcrypt.compare(password, user.passwordHash);
  if (!isValid) {
    throw new AuthenticationError('Invalid credentials');
  }
  
  // Generate JWT with user ID and role for authorization
  const token = jwt.sign(
    { userId: user._id, role: user.role },
    config.JWT_SECRET,
    { expiresIn: config.JWT_EXPIRES_IN }
  );
  
  return { token, user: user.toPublic() };
}
```

**Component Documentation:**
```typescript
/**
 * UserProfile Component
 * 
 * Displays and allows editing of user profile information.
 * Handles form validation and API calls for updates.
 * 
 * @param userId - The ID of the user to display/edit
 * @param isEditable - Whether the profile can be edited (default: false)
 * @param onUpdate - Callback fired when profile is successfully updated
 * 
 * State Management:
 * - Uses local state for form data
 * - Connects to user store for profile data
 * - Updates global auth state on profile changes
 * 
 * API Dependencies:
 * - GET /api/users/:id - Fetch user data
 * - PUT /api/users/:id - Update user data
 */
export const UserProfile: React.FC<UserProfileProps> = ({ userId, isEditable = false, onUpdate }) => {
  // Form state management - tracks dirty fields for save indication
  const [formData, setFormData] = useState<UserFormData>({});
  const [isDirty, setIsDirty] = useState(false);
  
  // API integration using React Query for caching and error handling
  const { data: user, isLoading, error } = useQuery(['user', userId], () => fetchUser(userId));
  
  // ... component logic
};
```

**API Endpoint Documentation:**
```typescript
/**
 * POST /api/auth/login
 * 
 * Authenticates user credentials and returns JWT token
 * 
 * Request Body:
 * - email: string (required) - User's email address
 * - password: string (required) - Plain text password
 * 
 * Response:
 * - 200: { token: string, user: UserPublic } - Successful authentication
 * - 401: { error: string } - Invalid credentials
 * - 422: { error: string, details: ValidationError[] } - Invalid input format
 * 
 * Security Notes:
 * - Rate limited to 5 attempts per minute per IP
 * - Password is hashed with bcrypt before comparison
 * - JWT expires in 7 days (configurable)
 */
router.post('/login', validate(loginSchema), async (req, res) => {
  try {
    // Extract and validate request data
    const { email, password } = req.body;
    
    // ... implementation
  } catch (error) {
    // ... error handling
  }
});
```

**2.2 Development Commands**
```bash
# Start development environment
npm run dev

# Work on specific components
npm run dev:frontend  # Frontend development
npm run dev:backend   # Backend development
```

**2.3 Quality Checks During Development**
```bash
# Run before each commit
npm run typecheck     # TypeScript validation
npm run lint          # Code style and quality
npm test              # Unit and integration tests
npm run build         # Build verification
```

### Phase 3: Deployment & Documentation Validation

**3.1 Documentation Validation Strategy**

**Validate Documentation Accuracy:**
After implementing code, verify that documentation created in Phase 1 is accurate:

1. **Test Architecture Documentation**
   ```bash
   # Verify that docs/architecture/ files match implementation
   # Check that data flow diagrams are correct
   # Validate security assumptions are implemented
   ```

2. **Test API Documentation Examples**
   ```bash
   # Run all code examples in docs/api/ files
   # Verify request/response formats are accurate
   # Test error scenarios documented
   ```

3. **Validate Feature Documentation**
   ```bash
   # Ensure docs/features/ accurately describe functionality
   # Test user workflows described in documentation
   ```

**3.2 README.md Synchronization**
Verify main README.md reflects current state:
- Installation steps work correctly
- Commands and scripts are up-to-date
- Technology stack is current
- Environment variables are complete
- Project structure matches reality

**3.3 Documentation Completeness Checklist**
- [ ] All planned documentation from Phase 1 updated
- [ ] Code examples in docs/ actually work
- [ ] API documentation matches implemented endpoints
- [ ] Architecture docs reflect actual implementation
- [ ] README.md navigation points to correct files
- [ ] Breaking changes documented in CHANGELOG.md

### Phase 4: Code Review & Quality Assurance

**4.1 Pre-PR Checklist**
```bash
# Final validation before creating PR
npm run typecheck:frontend && npm run typecheck:backend
npm run lint:frontend && npm run lint:backend  
npm run test:frontend && npm run test:backend
npm run build
```

**4.2 Commit Convention**
```bash
git commit -m "feat(auth): add JWT authentication system

- Implement user login/logout functionality
- Add JWT token validation middleware  
- Update user model with authentication fields
- Add comprehensive test coverage
- Update docs/api/authentication.md with new endpoints

Resolves: #123"
```

**4.3 Pull Request Creation**
Include in PR description:
- Purpose and changes made
- Documentation updates performed
- Testing completed
- Screenshots/demos for UI changes
- Breaking changes and migration steps

### Phase 5: Deployment Pipeline

**5.1 Merge to Develop**
```bash
# Triggers automatic staging deployment
git checkout develop
git merge --no-ff feature/ISSUE-123-user-authentication
git push origin develop
```

**5.2 Staging Validation**
- Test implemented functionality matches documented behavior
- Verify documentation examples work in staging environment
- Validate API responses match documented formats
- Confirm README instructions work on clean environment

**5.3 Production Release**
```bash
# Create release branch
git checkout -b release/v1.2.0

# Final documentation verification before production
# Update version numbers
# Create comprehensive release notes
# Merge to main for production deployment
```

---

# 2. CODING APPROACH

## 🏗️ Architecture-First Development Strategy

### Phase 1: Analysis Before Coding

**1.1 Architecture Review Process**
```bash
# ALWAYS start by reading these docs before coding:
docs/architecture/overview.md      # Understand system design
docs/architecture/frontend.md      # Frontend patterns and conventions  
docs/architecture/backend.md       # Backend architecture decisions
docs/architecture/database.md      # Data modeling and relationships
docs/architecture/security.md      # Security considerations
```

**1.2 Data Flow Analysis**
1. **Identify the complete data flow**
   - Where does data originate?
   - How does it flow through the system?
   - What transformations occur?
   - Where is it stored/cached?

2. **Map all touchpoints**
   - Frontend components affected
   - Backend services involved
   - Database tables/collections
   - External APIs or integrations
   - Shared utilities or middleware

**1.3 Impact Assessment**
```markdown
Before making changes, document:

**Upstream Dependencies:**
- What systems/components feed data to this feature?
- What happens if those systems change?
- Are there any assumptions that might break?

**Downstream Dependencies:**  
- What systems/components consume data from this feature?
- How will changes affect those consumers?
- Are there breaking changes that need coordination?

**Cross-cutting Concerns:**
- Authentication/authorization impacts
- Logging and monitoring changes needed
- Performance implications
- Security considerations
```

### Phase 2: Implementation Strategy

**2.1 Follow Established Patterns**
```bash
# Study existing code patterns before implementing
# Frontend: Look at similar components
find frontend/src -name "*.tsx" -type f | head -5 | xargs grep -l "useState\|useEffect"

# Backend: Study similar endpoints  
find backend/src -name "*.ts" -type f | head -5 | xargs grep -l "express\|router"
```

**2.2 Maintain Consistency**
- **Frontend**: Follow component structure, state management patterns
- **Backend**: Use established middleware, error handling, validation patterns
- **Database**: Follow naming conventions, relationship patterns
- **Testing**: Match existing test structure and coverage expectations

**2.3 Handle All Dependencies**
```typescript
// Example: Adding new user authentication feature

// 1. Update type definitions (upstream impact)
interface User {
  id: string;
  email: string;
  role: UserRole;        // ← New field affects all user interfaces
  lastLogin?: Date;      // ← New field affects user displays
}

// 2. Update all consuming components (downstream impact)
// - User profile components
// - Admin user management
// - Authentication middleware
// - Database queries
// - API responses

// 3. Update related services
// - Email notification service (role-based emails)
// - Audit logging (track role changes)
// - Permission checking (role-based access)
```

### Phase 3: Testing Strategy

**3.1 Test All Impact Areas**
```bash
# Test upstream dependencies
npm run test:integration  # Ensure data flows correctly

# Test downstream dependencies  
npm run test:unit        # Verify component behavior
npm run test:e2e         # End-to-end user journeys

# Test cross-cutting concerns
npm run test:security    # Security implications
npm run test:performance # Performance impact
```

**3.2 Documentation Testing**
- Verify all code examples in docs/ work correctly
- Test API documentation examples
- Validate README.md setup instructions

---

# 3. DEBUGGING

## 🔍 Systematic Debugging Approach

### Phase 1: Issue Isolation

**1.1 Information Gathering**
```bash
# Collect essential information
echo "Environment: $(node --version), $(npm --version)"
echo "Branch: $(git branch --show-current)"
echo "Last commit: $(git log -1 --oneline)"
echo "Changed files: $(git diff --name-only HEAD~1)"
```

**1.2 Reproduce the Issue**
```bash
# Create minimal reproduction case
npm run dev
# Document exact steps to reproduce
# Note expected vs actual behavior
# Capture error messages, logs, screenshots
```

**1.3 Log Analysis**
```bash
# Frontend debugging
# Check browser console, network tab, React DevTools

# Backend debugging  
# Check server logs, database queries, API responses
npm run dev:backend | grep -i error
```

### Phase 2: Root Cause Analysis

**2.1 Systematic Investigation**
```markdown
**Frontend Issues:**
1. Component state problems → Check React DevTools
2. API integration issues → Check Network tab
3. Routing problems → Verify React Router setup
4. Build issues → Check Vite/TypeScript errors

**Backend Issues:**
1. API endpoint problems → Check Express routing
2. Database issues → Verify MongoDB connections/queries  
3. Authentication failures → Check JWT middleware
4. External API problems → Check integration logs

**Infrastructure Issues:**
1. Deployment failures → Check CI/CD logs
2. Environment problems → Verify environment variables
3. Performance issues → Check monitoring dashboards
4. Security concerns → Review security logs
```

**2.2 Use Architecture Documentation**
```bash
# Reference architecture docs to understand expected behavior
cat docs/architecture/overview.md     # System design context
cat docs/architecture/database.md     # Data flow expectations
cat docs/api/standards.md             # API behavior standards
```

### Phase 3: Resolution Strategy

**3.1 Fix Implementation**
```bash
# Create debugging branch
git checkout -b bugfix/ISSUE-456-fix-login-error

# Implement minimal fix
# Focus on root cause, not symptoms
# Add tests to prevent regression
```

**3.2 Validation Process**
```bash
# Verify fix works
npm run test              # Run affected tests
npm run dev               # Manual testing
npm run build             # Build verification

# Test edge cases
# Verify no new issues introduced
# Check performance impact
```

**3.3 Documentation Updates**
```markdown
After fixing bugs, update:

**If Architecture Issue:**
- Update docs/architecture/ files
- Add troubleshooting section to docs/development/troubleshooting.md

**If API Issue:**  
- Update docs/api/ documentation
- Add error handling examples

**If Process Issue:**
- Update this CLAUDE.md file
- Add prevention steps to development workflow
```

### Phase 4: Prevention Strategies

**4.1 Add Monitoring/Logging**
```typescript
// Add debugging capabilities for future issues
import { logger } from '@/utils/logger';

export const authMiddleware = (req, res, next) => {
  logger.info('Auth middleware triggered', {
    path: req.path,
    method: req.method,
    timestamp: new Date().toISOString()
  });
  
  // ... middleware logic
};
```

**4.2 Improve Error Handling**
```typescript
// Frontend error boundaries
// Backend error middleware
// Database connection error handling
// API integration fallbacks
```

**4.3 Update Testing**
```bash
# Add tests for the bug scenario
# Improve test coverage for affected areas
# Add integration tests if missing
```

---

## 🛠️ Essential Commands Reference

```bash
# Development
npm run dev                    # Start all services
npm run dev:frontend          # Frontend only  
npm run dev:backend           # Backend only

# Quality Assurance
npm run typecheck             # Type checking
npm run lint                  # Code linting
npm run lint:fix              # Auto-fix linting issues
npm test                      # Run all tests
npm run test:watch            # Watch mode testing
npm run test:coverage         # Coverage report

# Build & Deploy
npm run build                 # Build applications
npm run install:all           # Install all dependencies
npm run clean                 # Clean build artifacts

# Debugging Tools
npm run dev:debug             # Debug mode (when implemented)
npm audit                     # Security audit
git log --oneline -10         # Recent commits
git diff HEAD~1               # Recent changes
```

---

**Last Updated:** December 2024  
**Version:** 1.0.0

This guide ensures systematic, architecture-aware development with comprehensive documentation and efficient debugging workflows.