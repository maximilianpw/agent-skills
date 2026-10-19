# Components and composition

## Component interfaces

Treat a component's props, accepted children, rendered semantics, controlled state, events, and error behavior as one interface.

- Use props for values, finite visual or behavioral variants, and callbacks describing user events.
- Use `children` for one caller-owned region and named `ReactNode` props for a small number of regions whose placement matters.
- Keep props immutable. Ask the owner to provide new values through callbacks rather than mutating received objects.
- Forward native props when the component genuinely preserves the native element's contract. Broad prop spreading through unrelated wrappers obscures ownership.
- Keep component functions at module scope. A component declared during another component's render has a new identity every render and resets its subtree.
- Call components through JSX so React owns identity, reconciliation, and Hooks.

### Composition over configuration

Prefer composition when a caller chooses substantial structure:

```tsx
<Panel>
  <PanelHeader>
    <Heading>Recent activity</Heading>
    <Actions>
      <Button>Refresh</Button>
    </Actions>
  </PanelHeader>
  <ActivityList />
</Panel>
```

A compact prop is clearer when the choice is finite and owned by the component:

```tsx
<Button variant="destructive" disabled={pending}>
```

Use these signals to replace configuration with composition:

- boolean props select which subtrees exist;
- arrays attempt to describe arbitrary JSX;
- render callbacks accumulate mainly as escape hatches rather than to provide owned state;
- caller-specific behavior leaks through escape-hatch props;
- adding one screen requires extending a generic renderer.

A typed configuration is appropriate for a closed vocabulary with uniform behavior, such as navigation destinations, status presentations, filter choices, or stable column metadata. Keep route registration, domain workflows, permission enforcement, and state transitions in their owning code rather than a parallel application schema.

## Compound components and context

Use compound components when several exported parts form one stable semantic pattern and need shared coordination. Keep ordinary wrappers ordinary when context adds no behavior.

- The root owns shared state or policy.
- Parts expose semantic roles rather than styling fragments.
- Fail clearly when a part requires a missing root.
- Keep value and dispatch/action contexts separate when read-only consumers should not rerender for action identity changes.
- Export a custom hook when it preserves an owned context contract, not merely to shorten `useContext`.

Avoid inspecting arbitrary `children` with `React.Children` to infer application structure. Prefer explicit child components or typed data when identity and ordering matter.

## State placement in component trees

For each unique state value, choose one owner:

- keep private interaction state near the leaf that uses it;
- lift state to the closest common parent when siblings coordinate;
- make a component controlled when the parent must coordinate or persist the value;
- keep a component uncontrolled when local ownership makes it simpler and no external coordination is required.

Controlled and uncontrolled are design choices, not maturity levels. Do not switch a form control between them during its lifetime.

## Lists, identity, and keys

- Use stable IDs from the data as keys.
- Keys are unique among siblings, not globally.
- Use an index only for a static list that cannot reorder, insert, or delete.
- Generate neither random keys nor `useId` list keys during render.
- Use an intentional key outside lists when a new entity, route identity, or form session must receive fresh state.

## Abstraction bar

Extract a component, hook, or pattern when it hides repeated behavior, accessibility policy, state transitions, or integration mechanics behind a smaller interface.

Prefer the direct composition when an abstraction would only:

- forward the same props;
- rename a framework hook;
- wrap every design-system primitive;
- move markup without creating an independent concept;
- require more concepts at the call site than the implementation it replaces.

Apply the deletion test: a deep abstraction earns its place when deleting it redistributes meaningful complexity across callers.

## Sources

- React, [Passing Props to a Component](https://react.dev/learn/passing-props-to-a-component)
- React, [Sharing State Between Components](https://react.dev/learn/sharing-state-between-components)
- React, [Thinking in React](https://react.dev/learn/thinking-in-react)
- React, [Preserving and Resetting State](https://react.dev/learn/preserving-and-resetting-state)
- React, [Rendering Lists](https://react.dev/learn/rendering-lists)
- React, [`Children` alternatives](https://react.dev/reference/react/Children#alternatives)
- React, [React calls Components and Hooks](https://react.dev/reference/rules/react-calls-components-and-hooks)
