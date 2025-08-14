# Components

No components were discovered in the repository yet. Add component docs here as your UI/library components are implemented.

## Template
Use `docs/templates/component.md` as a starting point for every component doc. Recommended sections:
- **Summary**: What the component does
- **Props/Inputs**: Name, type, required?, default
- **Events/Outputs**: Names and payloads
- **Accessibility**: Keyboard, ARIA, focus management
- **Styling/Theming**: How to customize appearance
- **Usage**: Minimal import and usage examples
- **Best Practices**: Do’s and don’ts

## Example (pseudo-code)
```tsx
// Example only — replace with your real component
import { Timeline } from "@app/components/Timeline"

export const Page = () => (
  <Timeline userId="123" pageSize={20} />
)
```