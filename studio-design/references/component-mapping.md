# Component Mapping — Pencil (.pen) ↔ React/shadcn/Radix

## Layout Containers

| .pen Pattern | React / Tailwind |
|-------------|-----------------|
| `frame` + `layout: "vertical"` | `<div className="flex flex-col gap-{n}">` |
| `frame` + `layout: "horizontal"` | `<div className="flex flex-row gap-{n} items-center">` |
| `frame` no layout | `<div className="relative">` + `absolute` children |
| `width: "fill_container"` | `flex-1` or `w-full` |
| `width: "fit_content"` | `w-fit` |
| `cornerRadius: 8` | `rounded-lg` |
| `stroke` + `strokeWidth` | `border border-border` |

## Spacing

| Pixels | Tailwind |
|--------|----------|
| 4 | `1` |
| 8 | `2` |
| 12 | `3` |
| 16 | `4` |
| 20 | `5` |
| 24 | `6` |
| 32 | `8` |

Non-standard: `gap-[10px]`, `p-[18px]`

## Text

| .pen | React / Tailwind |
|------|-----------------|
| `fontSize: 24, fontWeight: 700` | `<h1 className="text-2xl font-bold">` |
| `fontSize: 20, fontWeight: 600` | `<h2 className="text-xl font-semibold">` |
| `fontSize: 14, fontWeight: 400` | `<span className="text-sm">` |
| `fontSize: 12` | `<span className="text-xs">` |
| `fill: "$text-primary"` | `text-foreground` |
| `fill: "$text-secondary"` | `text-muted-foreground` |

## Icons

| .pen | React |
|------|-------|
| `iconFontFamily: "lucide"` | `import { XxxIcon } from "lucide-react"` |
| `iconFontName: "panel-left"` | `<PanelLeftIcon />` |
| `width: 16` | `className="size-4"` |
| `width: 18` | `className="size-[18px]"` |
| `width: 20` | `className="size-5"` |

Name conversion: `kebab-case` → `PascalCase` + `Icon` (e.g., `message-square` → `MessageSquareIcon`)

## UI Components

### Buttons
| .pen | shadcn |
|------|--------|
| `frame` + `text` + accent fill | `<Button>` (default) |
| `frame` + `text` + border only | `<Button variant="outline">` |
| `frame` + `text` + no fill | `<Button variant="ghost">` |
| `frame` + icon only | `<Button variant="ghost" size="icon">` |

### Inputs
| .pen | shadcn |
|------|--------|
| `frame` + placeholder text + `$bg-input` fill | `<Input />` |
| `frame` + search icon + text + `$bg-input` | Search input with icon |
| Multi-line + `$bg-input` | `<Textarea />` |

### Cards
| .pen | shadcn |
|------|--------|
| `frame` + `$bg-card` + `$border` + radius | `<Card>` |
| Bold text inside card | `<CardTitle>` |
| Content inside card | `<CardContent>` |

### Sidebar
| .pen | shadcn |
|------|--------|
| `frame` width=260, `$bg-sidebar` | `<Sidebar>` |
| Logo/brand area | `<SidebarHeader>` |
| Nav items | `<SidebarContent>` + `<SidebarMenu>` |
| Nav item row | `<SidebarMenuItem>` + `<SidebarMenuButton>` |
| User info bottom | `<SidebarFooter>` |

### Dropdown
| .pen | shadcn |
|------|--------|
| Trigger + chevron-down | `<DropdownMenuTrigger>` |
| Menu container + `$bg-card` | `<DropdownMenuContent>` |
| Menu item row | `<DropdownMenuItem>` |

### Dialog
| .pen | shadcn |
|------|--------|
| Overlay + centered content | `<Dialog>` |
| Title in dialog | `<DialogTitle>` |
| Actions row | `<DialogFooter>` |

## Color Mapping

| .pen Token | Tailwind |
|-----------|----------|
| `$bg` | `bg-background` |
| `$bg-sidebar` | `bg-sidebar` |
| `$bg-card` | `bg-card` |
| `$bg-input` | `bg-input` |
| `$text-primary` | `text-foreground` |
| `$text-secondary` | `text-muted-foreground` |
| `$accent` | `bg-primary` |
| `$border` | `border-border` |
| `$destructive` | `text-destructive` |
