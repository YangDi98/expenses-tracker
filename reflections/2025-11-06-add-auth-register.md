### Feature
Add Auth Flow Register and Login

### Notes
- username and email is stored in lowercase letters, and they have to be unique
- Best Practices for JWT Secret Keys:
  - Length: At least 256 bits (32 bytes) for HS256 algorithm
  - Randomness: Use cryptographically secure random generators
  - Storage: Store in environment variables, never in code
  - Rotation: Regularly rotate your secret keys
  - Environment-specific: Use different keys for development, staging, and production
