#pragma once
#include <windef.h>
#include <stdbool.h>

typedef struct KeyConfig
{
    unsigned int _AppHold;
    unsigned int _AppSwitch;
    unsigned int _WinHold;
    unsigned int _WinSwitch;
    unsigned int _Invert;
    unsigned int _PrevApp;
} KeyConfig;

typedef enum ThemeMode
{
    ThemeModeAuto,
    ThemeModeLight,
    ThemeModeDark
} ThemeMode;

typedef enum DisplayName
{
    DisplayNameSel,
    DisplayNameAll,
    DisplayNameNone
} DisplayName;

typedef enum AppSwitcherMode
{
    AppSwitcherModeApp,
    AppSwitcherModeWindow,
} AppSwitcherMode;

typedef struct Config
{
    KeyConfig _Key;
    bool _Mouse;
    bool _CheckForUpdates;
    ThemeMode _ThemeMode;
    DisplayName _DisplayName;
    float _Scale;
    AppSwitcherMode _AppSwitcherMode;
} Config;

typedef struct EnumString
{
    const char* Name;
    unsigned int Value;
} EnumString;

extern const EnumString keyES[14];
extern const EnumString themeES[4];
extern const EnumString appSwitcherModeES[3];
extern const EnumString displayNameES[4];

void LoadConfig(Config* config);
void WriteConfig(const Config* config);