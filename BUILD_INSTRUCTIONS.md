# Build Instructions for ag-ui

## Issue: Missing Protocol Buffers Compiler (protoc)

The build is failing because `protoc` (Protocol Buffers compiler) is not installed on your system.

### Quick Fix Applied

I've created placeholder files in `typescript-sdk/packages/proto/src/generated/` to allow the build to proceed without protoc. This is a temporary workaround.

### Permanent Solution

To properly build the project with full protobuf support:

1. **Install protoc on Windows:**
   - Download from: https://github.com/protocolbuffers/protobuf/releases
   - Extract and add to PATH
   - Or use Chocolatey: `choco install protoc`

2. **After installing protoc:**
   - Delete the placeholder files in `typescript-sdk/packages/proto/src/generated/`
   - Re-enable DTS generation in `typescript-sdk/packages/proto/tsup.config.ts` (change `dts: false` back to `dts: true`)
   - Run `pnpm install` and `pnpm build`

### Current Build Status

✅ Core packages build successfully:
- @ag-ui/core
- @ag-ui/proto (with placeholders)
- @ag-ui/encoder
- @ag-ui/client
- All integration packages

❌ Demo app fails due to Next.js issue (separate from protoc issue)

### Commands

```bash
# Build all packages
cd typescript-sdk
pnpm install
pnpm build

# Build specific package
pnpm build --filter=@ag-ui/core
```