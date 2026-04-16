# Skill: Autonomous Web Browsing

## Description and Purpose

This skill describes the native capability of Ideas-brillantes to autonomously browse the web using a Playwright-based browser automation layer. The model operates in a perception-action loop: it observes the current state of the page (DOM snapshot, screenshot, or both), decides on the next action, executes it, and re-evaluates until the task is complete. This behavior is embedded — the model understands browser semantics natively and does not need to be taught how to browse.

---

## When This Skill Applies

- User asks to search for information online ("find the latest news about X")
- User asks to navigate to a specific website
- User asks to fill out a web form or submit data
- User asks to extract structured data from a webpage (scraping)
- User needs to log into a website (with provided credentials)
- User asks to monitor a page for changes
- User asks to download a file from the web
- Multi-step research tasks that require visiting several pages

---

## Perception-Action Loop

The browser operates in a continuous cycle:

```
OBSERVE → PLAN → ACT → OBSERVE → PLAN → ACT → ... → DONE
```

1. **OBSERVE:** Receive current page state — URL, title, visible text, interactive elements (links, buttons, inputs), and optionally a screenshot.
2. **PLAN:** Determine the next single action needed to progress toward the goal.
3. **ACT:** Execute the action via a tool call.
4. **EVALUATE:** Check if the goal is achieved. If yes, return results. If no, loop.

The model maintains internal state about:
- Current URL and page history
- Actions taken so far
- Partial results accumulated
- Whether progress is being made (loop detection)

---

## Core Behaviors

### 1. Navigation

**Direct URL navigation:**
```
Tool: browser_navigate
  url: "https://example.com"
  wait_until: "networkidle"    # wait for page to fully load
```

**Going back/forward:**
```
Tool: browser_navigate
  action: "back"

Tool: browser_navigate
  action: "forward"
```

**Opening new tab:**
```
Tool: browser_new_tab
  url: "https://example.com"
```

**Refreshing:**
```
Tool: browser_navigate
  action: "reload"
```

---

### 2. Web Search

**Google Search:**
```
Tool: browser_navigate
  url: "https://www.google.com/search?q=your+query+here"

# Or navigate to Google and type:
Tool: browser_navigate
  url: "https://www.google.com"

Tool: browser_type
  selector: "textarea[name='q']"
  text: "your search query"

Tool: browser_key
  key: "Enter"
```

**DuckDuckGo (preferred for privacy):**
```
Tool: browser_navigate
  url: "https://duckduckgo.com/?q=your+query+here"
```

**Reading search results:**
```
Tool: browser_extract
  selector: "#search .g"           # Google result items
  fields: ["title", "url", "snippet"]

# Or extract all visible text:
Tool: browser_get_text
  selector: "body"
```

---

### 3. Extracting Content from Pages

**Get all text:**
```
Tool: browser_get_text
  selector: "body"
  # Returns visible text, strips HTML

Tool: browser_get_text
  selector: "article"    # main content area
```

**Extract structured data:**
```
Tool: browser_extract
  selector: "table"
  format: "markdown_table"

Tool: browser_extract
  selector: ".product-card"
  fields: ["name", "price", "rating"]
  multiple: true          # extract all matching elements
```

**Get page HTML:**
```
Tool: browser_get_html
  selector: "main"        # scoped to element
  clean: true             # strip scripts/styles
```

**Get current URL and title:**
```
Tool: browser_get_state
  # Returns: { url, title, ready_state }
```

---

### 4. Filling Forms

**Text inputs:**
```
Tool: browser_type
  selector: "input[name='email']"
  text: "user@example.com"
  clear_first: true        # clear any existing value
```

**Passwords:**
```
Tool: browser_type
  selector: "input[type='password']"
  text: "password_value"
```

**Select dropdowns:**
```
Tool: browser_select
  selector: "select[name='country']"
  value: "ES"              # value attribute
  # OR
  label: "Spain"           # visible text
```

**Checkboxes and radio buttons:**
```
Tool: browser_click
  selector: "input[type='checkbox'][name='agree']"

Tool: browser_click
  selector: "input[type='radio'][value='option2']"
```

**Clicking buttons:**
```
Tool: browser_click
  selector: "button[type='submit']"
  # OR by text:
  text: "Sign In"
  # OR by coordinates (fallback):
  x: 540, y: 320
```

**Submitting forms:**
```
Tool: browser_click
  selector: "form button[type='submit']"
# Or:
Tool: browser_key
  key: "Enter"
```

---

### 5. Taking Screenshots

```
Tool: browser_screenshot
  full_page: false        # viewport only (default)
  path: "/tmp/page.png"  # optional save path

Tool: browser_screenshot
  full_page: true         # entire scrollable page
  selector: ".chart"      # optional: crop to element
```

Screenshots are used:
- To verify the current page state visually
- When the DOM extraction is insufficient (canvas, SVG, complex layouts)
- To provide evidence of task completion to the user
- For debugging unexpected page states

---

### 6. Handling Pagination

**Click "Next" button pattern:**
```
loop:
  Tool: browser_extract
    selector: ".item"
    multiple: true
    # accumulate results

  Tool: browser_click
    selector: "a.next-page, button[aria-label='Next']"
    # if not found → exit loop

  Tool: browser_wait
    condition: "networkidle"
```

**URL-based pagination:**
```
for page in 1..N:
  Tool: browser_navigate
    url: f"https://example.com/items?page={page}"
  # extract data
```

**Infinite scroll:**
```
loop:
  Tool: browser_scroll
    direction: "down"
    amount: "page"
  Tool: browser_wait
    milliseconds: 1500
  # check if new content loaded
  # exit when no new content appears
```

---

### 7. CAPTCHA Awareness

The model recognizes when it encounters a CAPTCHA and handles it appropriately:

**Detection patterns:**
- URL contains: `captcha`, `challenge`, `verify`
- Page contains: reCAPTCHA iframe, hCaptcha, Cloudflare challenge
- HTTP 403 or "Access Denied" responses
- Page text includes: "verify you are human", "prove you're not a robot"

**Behavior when CAPTCHA is detected:**
1. Take a screenshot and show it to the user
2. Clearly explain that a CAPTCHA has been encountered
3. Ask the user to solve it manually (if interactive session)
4. After user signals completion, take screenshot to verify and continue
5. NEVER attempt to bypass or automatically solve CAPTCHAs

```
# CAPTCHA encountered:
Tool: browser_screenshot
# → Show to user

Response: "I've encountered a CAPTCHA on this page. Please solve it 
in the browser window and let me know when you're done, 
and I'll continue from there."
```

---

### 8. Loop Detection and Recovery

The model monitors for signs of being stuck:

**Detecting a loop:**
- Same URL visited 3+ times with same content
- Same action attempted 3+ times without page change
- Error message appearing repeatedly
- No progress toward goal after 5+ actions

**Recovery strategies:**

1. **Try alternative selector:** Different CSS selector for the same element
2. **Scroll to element:** Element may be out of viewport
   ```
   Tool: browser_scroll_to
     selector: "#target-button"
   ```
3. **Wait and retry:** Dynamic content may not have loaded
   ```
   Tool: browser_wait
     condition: "element_visible"
     selector: "#dynamic-content"
     timeout: 5000
   ```
4. **Try different approach:** Search differently, use alternative URL
5. **Escalate to user:** If 3 recovery attempts fail, explain the issue

---

## Examples of Complex Web Tasks

### Example 1: Research task with multiple sources
```
User: "Find the top 3 Python web frameworks by GitHub stars and compare them"

Step 1:
Tool: browser_navigate
  url: "https://github.com/search?q=python+web+framework&s=stars&type=repositories"

Step 2:
Tool: browser_extract
  selector: ".repo-list-item"
  fields: ["name", "stars", "description"]
  multiple: true
  limit: 10

Step 3: Navigate to each top framework's repo to get details
Tool: browser_navigate
  url: "https://github.com/pallets/flask"
Tool: browser_get_text
  selector: "#readme"

# Repeat for Django, FastAPI...

Step 4: Synthesize and return comparison table to user
```

### Example 2: Form submission
```
User: "Fill out the contact form at example.com/contact with my info"

Tool: browser_navigate
  url: "https://example.com/contact"

Tool: browser_screenshot   # verify page loaded

Tool: browser_type
  selector: "input[name='name']"
  text: "User Name"

Tool: browser_type
  selector: "input[name='email']"
  text: "user@email.com"

Tool: browser_type
  selector: "textarea[name='message']"
  text: "Message content..."

# Show preview screenshot before submitting
Tool: browser_screenshot

# User confirms → submit
Tool: browser_click
  selector: "button[type='submit']"

Tool: browser_screenshot   # confirm success message
```

### Example 3: Monitoring a page for changes
```
User: "Check if the price of product X on site Y has dropped below $50"

loop every 30 minutes:
  Tool: browser_navigate
    url: "https://shop.example.com/product/X"

  Tool: browser_extract
    selector: ".price"
    # → "$47.99"

  if price < 50:
    notify_user("Price dropped to $47.99!")
    break
```

### Example 4: Multi-step login and data extraction
```
User: "Log into my account on X and get my recent orders"

Tool: browser_navigate
  url: "https://shop.example.com/login"

Tool: browser_type
  selector: "#email"
  text: [user_provided_email]

Tool: browser_type
  selector: "#password"
  text: [user_provided_password]

Tool: browser_click
  selector: "button[type='submit']"

Tool: browser_wait
  condition: "url_contains"
  value: "/dashboard"

Tool: browser_navigate
  url: "https://shop.example.com/account/orders"

Tool: browser_extract
  selector: ".order-row"
  fields: ["order_id", "date", "total", "status"]
  multiple: true

# Return data to user as formatted table
```

---

## Important Constraints

- **Never store passwords** in memory or logs beyond the immediate session action
- **Respect robots.txt** conceptually — avoid aggressive scraping
- **Rate limiting awareness:** Add waits between requests when scraping multiple pages
- **User confirmation required** before: form submission, purchases, login with credentials, any destructive action
- **Content policy:** Do not browse to or extract content from sites that violate content policies
