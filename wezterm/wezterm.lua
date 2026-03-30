local wezterm = require 'wezterm'
local config = wezterm.config_builder()
local act = wezterm.action

-- Load Dynamic Theme Info
local globals = dofile(wezterm.config_dir .. '/globals.lua')

-- Theme Selection Logic
local function active_theme()
  return globals.preview_theme or globals.current_theme
end

config.color_scheme = active_theme()

config.colors = {
  tab_bar = {
    background = 'rgba(0,0,0,0)',
  }
}

-- Font Configuration
config.font = wezterm.font_with_fallback {
  'JetBrains Mono',
  'JetBrainsMono Nerd Font',
  'monospace',
}
config.font_size = 14.0

-- Window Appearance
config.window_background_opacity = 0.9
config.window_padding = {
  left = 48,
  right = 48,
  top = 48,
  bottom = 48,
}
config.window_decorations = "NONE"
config.check_for_updates = false

-- Waybar-Style Tab Bar Configuration
config.use_fancy_tab_bar = false
config.tab_bar_at_bottom = true
config.hide_tab_bar_if_only_one_tab = false
config.tab_max_width = 32

-- COLORS (Match Waybar)
local WAYBAR_BG = '#101116'
local WAYBAR_ACCENT = '#5f87af' 
local WAYBAR_TEXT = '#ffffff'

----------------------------------------------------------------------
-- THEME SWITCHER LOGIC
----------------------------------------------------------------------
local function theme_switcher(window, pane)
  window:perform_action(
    act.SplitPane {
      direction = "Right",
      size = { Percent = 30 },
      command = {
        args = {
          "bash",
          "-c",
          string.format([[ 
WEZTERM_DIR="%s"
REPO_DIR="$WEZTERM_DIR/wezthemes_repo"

CURRENT_THEME=$(lua -e "
  local g = dofile('$WEZTERM_DIR/globals.lua')
  print(g.current_theme)
")

THEME_LIST=$(lua -e "
  local t = dofile('$WEZTERM_DIR/theme.lua')
  for _, v in ipairs(t) do print(v) end
")

if ! command -v fzf &> /dev/null; then
    echo "fzf not found. Please install it to use the theme switcher."
    exit 1
fi

SELECTED=$(echo "$THEME_LIST" | fzf --reverse --exact \
  --prompt="🎨 Theme (current: $CURRENT_THEME) > " \
  --bind "focus:execute-silent:sleep 0.01; lua $REPO_DIR/scripts/preview_theme.lua {}")

if [ -n "$SELECTED" ]; then
  lua "$REPO_DIR/scripts/apply_theme.lua" "$SELECTED"
else
  lua "$REPO_DIR/scripts/cancel_theme.lua"
fi
          ]],
          wezterm.config_dir
          )
        },
      },
    },
    pane
  )
end

----------------------------------------------------------------------
-- EVENTS (Tab Title & Status Bar)
----------------------------------------------------------------------

wezterm.on('format-tab-title', function(tab, tabs, panes, config, hover, max_width)
  local title = tab.active_pane.title
  
  -- Simple icon selection
  local icon = wezterm.nerdfonts.dev_terminal .. " "
  local p_name = tab.active_pane.foreground_process_name:lower()
  if p_name:find("nvim") or p_name:find("vim") then icon = wezterm.nerdfonts.custom_neovim .. " " end
  if p_name:find("git") then icon = wezterm.nerdfonts.dev_git .. " " end
  if p_name:find("node") then icon = wezterm.nerdfonts.dev_nodejs_small .. " " end
  if p_name:find("python") then icon = wezterm.nerdfonts.dev_python .. " " end

  local text = "  " .. icon .. title .. "  "

  if tab.is_active then
    return {
      { Background = { Color = WAYBAR_ACCENT } },
      { Foreground = { Color = WAYBAR_TEXT } },
      { Attribute = { Intensity = 'Bold' } },
      { Text = text },
      { Background = { Color = 'rgba(0,0,0,0)' } },
      { Text = '  ' },
    }
  elseif hover then
    return {
      { Background = { Color = 'rgba(95, 135, 175, 0.2)' } },
      { Foreground = { Color = WAYBAR_ACCENT } },
      { Text = text },
      { Background = { Color = 'rgba(0,0,0,0)' } },
      { Text = '  ' },
    }
  else
    return {
      { Background = { Color = WAYBAR_BG } },
      { Foreground = { Color = WAYBAR_ACCENT } },
      { Text = text },
      { Background = { Color = 'rgba(0,0,0,0)' } },
      { Text = '  ' },
    }
  end
end)

wezterm.on('update-status', function(window, pane)
  -- 1. Watcher for alias 'weztheme'
  local f1 = io.open('/tmp/wezterm_trigger_theme_switcher', 'r')
  if f1 then
    f1:close()
    os.remove('/tmp/wezterm_trigger_theme_switcher')
    theme_switcher(window, pane)
    return
  end

  -- 2. Waybar-style Right Status
  local date = wezterm.strftime('%H:%M')
  local workspace = window:active_workspace()
  
  window:set_right_status(wezterm.format({
    { Background = { Color = WAYBAR_BG } },
    { Foreground = { Color = WAYBAR_ACCENT } },
    { Text = ' 󱂬 ' .. workspace .. ' ' },
    { Background = { Color = 'rgba(0,0,0,0)' } },
    { Text = '  ' },
    { Background = { Color = WAYBAR_BG } },
    { Foreground = { Color = WAYBAR_ACCENT } },
    { Attribute = { Intensity = 'Bold' } },
    { Text = ' 󱑎 ' .. date .. ' ' },
  }))
end)

----------------------------------------------------------------------
-- SMART PASTE (Image as Path for Gemini CLI)
----------------------------------------------------------------------
local function paste_image_as_path(window, pane)
  local tmp_dir = os.getenv("HOME") .. "/Pictures/wezterm_pastes"
  os.execute("mkdir -p " .. tmp_dir)

  -- Use wl-paste to check for image data
  local success, stdout, stderr = wezterm.run_child_process({ "wl-paste", "--list-types" })
  if success and stdout:find("image/png") then
    local filename = "paste_" .. os.date("%Y%m%d_%H%M%S") .. ".png"
    local full_path = tmp_dir .. "/" .. filename
    
    local save_success, save_stdout, save_stderr = wezterm.run_child_process({
      "wl-paste", "--type", "image/png", "--no-newline"
    })
    
    if save_success and #save_stdout > 0 then
      local file = io.open(full_path, "wb")
      if file then
        file:write(save_stdout)
        file:close()
        -- Send path prefixed with @ for Gemini CLI
        window:perform_action(act.SendString("@" .. full_path), pane)
        return
      end
    end
  end

  -- Fallback to normal text paste
  window:perform_action(act.PasteFrom 'Clipboard', pane)
end

----------------------------------------------------------------------
-- CONFIG REMAINING
----------------------------------------------------------------------

config.scrollback_lines = 5000
config.default_cursor_style = 'BlinkingBlock'
config.cursor_blink_rate = 500

config.mouse_bindings = {
  {
    event = { Up = { streak = 1, button = 'Left' } },
    mods = 'NONE',
    action = act.CompleteSelectionOrOpenLinkAtMouseCursor 'Clipboard',
  },
}

config.keys = {
  { key = '%', mods = 'CTRL|SHIFT', action = act.SplitPane { direction = 'Right', size = { Percent = 50 } } },
  { key = '"', mods = 'CTRL|SHIFT', action = act.SplitPane { direction = 'Down', size = { Percent = 50 } } },
  { key = 'LeftArrow', mods = 'CTRL|SHIFT', action = act.ActivateTabRelative(-1) },
  { key = 'RightArrow', mods = 'CTRL|SHIFT', action = act.ActivateTabRelative(1) },
  { key = 'c', mods = 'CTRL', action = act.CopyTo 'Clipboard' },
  { key = 'v', mods = 'CTRL', action = wezterm.action_callback(paste_image_as_path) },
}

return config
