# Forms and accessibility

Accessibility is part of the component interface: semantics, name, keyboard behavior, focus, announcements, content resilience, and recovery are caller-visible behavior.

## Form ownership

Choose intentionally between controlled and uncontrolled fields.

- Controlled inputs receive `value` or `checked` and update synchronously in `onChange`.
- Uncontrolled inputs receive initial `defaultValue` or `defaultChecked` and let the DOM retain the current value.
- Do not switch one control between controlled and uncontrolled during its lifetime.
- Keep one owner for each draft value. Avoid mirroring props into local field state unless the form session has an explicit identity and reset policy.
- Reset a conceptually new form session by unmounting or keying it by operation/entity identity rather than resetting many fields in an Effect.

A form library may own field values, touched state, validation timing, and submission state. Follow its documented field composition interface: for example, TanStack Form's `form.Field` children function is the supported way to expose field-owned state, not an application escape hatch. The library does not automatically own the surrounding product lifecycle:

- dirty or default-value semantics;
- discard confirmation;
- pending-close prevention;
- idempotency and duplicate submission;
- conflict or stale-record recovery;
- cache invalidation and authority refresh;
- success feedback, close behavior, and focus restoration.

Keep those policies explicit in an owned form or dialog pattern. Adopt a form library when it reduces the complete policy and test surface, not to make forms nominally uniform.

## Compositional form patterns

Prefer a pattern that owns repeated interaction and accessibility behavior while callers compose feature-specific fields:

```tsx
<FormDialog.Root dirty={dirty} pending={pending}>
  <FormDialog.Header>
    <FormDialog.Title>Edit product</FormDialog.Title>
    <FormDialog.Description>...</FormDialog.Description>
  </FormDialog.Header>
  <FormDialog.Errors>{summary}</FormDialog.Errors>
  <FormDialog.Fields>{fields}</FormDialog.Fields>
  <FormDialog.Actions>{actions}</FormDialog.Actions>
</FormDialog.Root>
```

The pattern may own close interception, discard confirmation, error-summary focus, and pending controls. It should not need a field-schema DSL capable of describing every workflow.

Validate untrusted submissions at the server boundary even when client validation exists. Client validation improves feedback; it is not the authoritative contract or authorization boundary.

## Native semantics first

Use the native element whose behavior matches the interaction:

- `button` for an action;
- `a` for navigation;
- `input`, `select`, and `textarea` for ordinary fields;
- `header`, `nav`, `main`, `aside`, and `footer` for landmarks;
- headings in a meaningful hierarchy;
- semantic tables for tabular relationships;
- the native `dialog` element when its behavior meets the product contract, or a proven headless dialog primitive when richer focus and overlay behavior is required.

A custom ARIA role is a promise to implement the expected keyboard, focus, state, and naming behavior. Prefer a proven headless primitive when a native control cannot express the interaction.

## Names, labels, instructions, and errors

- Give every control an accessible name through visible text or an associated `label` where practical.
- Use `htmlFor` plus a stable ID, or wrap the control in its label.
- Use React `useId` for component-instance IDs, not list keys.
- Connect descriptions and field errors with `aria-describedby`.
- Mark invalid fields with `aria-invalid` when invalidity is known.
- Put a form-level summary before the fields when several errors need review; focus it after a failed submit without removing each field's own association.
- Keep instructions and errors available as text rather than color, icon, or placeholder alone.

## Keyboard and focus

All functionality must be keyboard operable without a trap.

- Keep DOM, visual, and focus order aligned.
- Use native tab order. Never use positive `tabIndex` to repair structure.
- Preserve a visible focus indicator and forced-colors behavior.
- Move focus only for a user-understandable reason: opening a modal, completing navigation, reporting validation failure, or restoring the invoking control.
- Restore focus to the trigger after overlays close; if the trigger was deleted, choose a deterministic nearby fallback.
- Prevent focus from being obscured by sticky chrome or overlays.
- Test open, close, Escape, selection, destructive confirmation, and focus restoration for composite widgets.

## Dialogs and durable commands

A dialog owns one focus scope and a clear title/description. While an operation is pending:

- expose pending status;
- prevent duplicate submission;
- either support real cancellation through the operation owner or prevent dismissal from implying cancellation;
- preserve the result and recovery path if the operation settles after navigation or closure.

Durable or irreversible commands need explicit confirmation and should not disappear while continuing unless the UI clearly communicates background execution.

## Status and asynchronous feedback

Use an appropriate live region or status role for important asynchronous outcomes that do not move focus. Avoid announcing every loading tick. Keep error details and request/correlation IDs selectable and readable without exposing private response bodies.

## Reflow, content, and localization

- Support the repository's declared viewport and zoom matrix; WCAG Reflow uses a 320 CSS-pixel equivalent for ordinary vertical content.
- Keep document overflow out of ordinary pages. A genuinely two-dimensional table may scroll in its own named region.
- Test long translated labels, unbroken identifiers, quantities, dates, empty content, and user-generated names.
- Set the document language and mark language changes on the smallest enclosing element.
- Preserve required actions and information at narrow widths rather than hiding them.
- Meet WCAG 2.2 AA's 24-by-24 CSS-pixel minimum target size or one of its documented spacing and semantic exceptions.

## Motion and visual state

Honor `prefers-reduced-motion`. Do not make status, selection, errors, or required actions depend only on color or animation. Verify text and non-text contrast in the actual component states, including focus, disabled, selected, invalid, and forced colors.

## Sources

- React, [`input`](https://react.dev/reference/react-dom/components/input)
- React, [`select`](https://react.dev/reference/react-dom/components/select)
- React, [`textarea`](https://react.dev/reference/react-dom/components/textarea)
- React, [`useId`](https://react.dev/reference/react/useId)
- React, [Preserving and Resetting State](https://react.dev/learn/preserving-and-resetting-state)
- TanStack Form, [Basic Concepts](https://tanstack.com/form/latest/docs/framework/react/guides/basic-concepts)
- TanStack Form, [Form Composition](https://tanstack.com/form/latest/docs/framework/react/guides/form-composition)
- WAI-ARIA APG, [Read Me First](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/)
- WAI-ARIA APG, [Keyboard Interface](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/)
- WCAG 2.2, [Keyboard](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html)
- WCAG 2.2, [Focus Not Obscured](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html)
- WCAG 2.2, [Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html)
- WCAG 2.2, [Status Messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html)
- WCAG 2.2, [Target Size](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)
- WCAG 2.2, [Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)
- WCAG 2.2, [Non-text Contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)
- web.dev, [Semantic HTML](https://web.dev/learn/html/semantic-html)
- web.dev, [Focus](https://web.dev/learn/accessibility/focus)
