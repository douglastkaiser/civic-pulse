import js from '@eslint/js'
import hooks from 'eslint-plugin-react-hooks'
export default [
  { ignores: ['node_modules/**', 'dist/**', 'public/**', 'playwright-report/**', 'test-results/**'] },
  js.configs.recommended,
  { files: ['**/*.{js,jsx}'], languageOptions: { ecmaVersion: 'latest', sourceType: 'module', parserOptions: { ecmaFeatures: { jsx: true } }, globals: { getComputedStyle: 'readonly', window: 'readonly', document: 'readonly', navigator: 'readonly', localStorage: 'readonly', fetch: 'readonly', URL: 'readonly', Blob: 'readonly', AbortController: 'readonly', AbortSignal: 'readonly', crypto: 'readonly', TextEncoder: 'readonly', console: 'readonly', setTimeout: 'readonly', clearTimeout: 'readonly', process: 'readonly', __COMMIT_HASH__: 'readonly', structuredClone: 'readonly' } }, rules: { 'no-unused-vars': 'off' } },
  { files: ['src/**/*.{js,jsx}'], plugins: { 'react-hooks': hooks }, rules: { 'react-hooks/rules-of-hooks': 'error', 'react-hooks/exhaustive-deps': 'warn' } },
]
