#include <windows.h>
#include <cstdlib>
#include <string>
#include <tchar.h>
#include <filesystem>
#include <thread>
#include <iostream>

static TCHAR szWindowClass[] = _T("CourseProject");

static TCHAR szTitle[] = _T("CourseProject");

std::wstring fullPath = std::filesystem::current_path().wstring() + L"\\pythonscript.exe";

HINSTANCE hInst;

LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);

int WINAPI WinMain( _In_ HINSTANCE hInstance,
                    _In_opt_ HINSTANCE hPrevInstance,
                    _In_ LPSTR     lpCmdLine,
                    _In_ int       nCmdShow)
{
    WNDCLASSEX wcex;

    wcex.cbSize = sizeof(WNDCLASSEX);
    wcex.style = CS_HREDRAW | CS_VREDRAW;
    wcex.lpfnWndProc = WndProc;
    wcex.cbClsExtra = 0;
    wcex.cbWndExtra = 0;
    wcex.hInstance = hInstance;
    wcex.hIcon = LoadIcon(wcex.hInstance, IDI_APPLICATION);
    wcex.hCursor = LoadCursor(nullptr, IDC_ARROW);
    wcex.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wcex.lpszMenuName = nullptr;
    wcex.lpszClassName = szWindowClass;
    wcex.hIconSm = LoadIcon(wcex.hInstance, IDI_APPLICATION);

    if (!RegisterClassEx(&wcex))
    {
        MessageBox(nullptr,
                   _T("Call to RegisterClassEx failed!"),
                   _T("Windows Desktop Guided Tour"),
                   NULL);

        return 1;
    }

    hInst = hInstance;

    HWND hWnd = CreateWindowEx(
            WS_EX_OVERLAPPEDWINDOW,
            szWindowClass,
            szTitle,
            WS_OVERLAPPEDWINDOW,
            CW_USEDEFAULT, CW_USEDEFAULT,
            1000, 700,
            nullptr,
            nullptr,
            hInstance,
            nullptr
    );

    if (!hWnd)
    {
        MessageBox(nullptr,
                   _T("Call to CreateWindow failed!"),
                   _T("Windows Desktop Guided Tour"),
                   NULL);

        return 1;
    }


    ShowWindow(hWnd, nCmdShow);
    ShowWindow(::GetConsoleWindow(), SW_HIDE);
    UpdateWindow(hWnd);

    // Main message loop:
    MSG msg;
    while (GetMessage(&msg, nullptr, 0, 0))
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return (int)msg.wParam;
}

LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
{
    PAINTSTRUCT ps;
    HDC hdc;
    TCHAR greeting[] = _T("Extracting key attributes from a resume (Russian)");
    WCHAR inscription[] = L"Выберите файлы разрешения: \n.pdf .docx или .txt \nдля извлечения ключевых атрибутов";
    static HWND hwndButton;
    static int x = 420;
    static int y = 10;
    static HFONT hFont = nullptr;

    switch (message)
    {
        case WM_PAINT:
        {
            hdc = BeginPaint(hWnd, &ps);

            auto hOldFont = (HFONT)SelectObject(hdc, hFont);


            TextOut(hdc, x, y,greeting, _tcslen(greeting));

            RECT rect;
            GetClientRect(hWnd, &rect);
            DrawTextW(hdc, inscription, -1, &rect, DT_CENTER | DT_VCENTER | DT_SINGLELINE);

            SelectObject(hdc, hOldFont);
            EndPaint(hWnd, &ps);

            break;
        }
        case WM_CREATE:
        {
            hwndButton = CreateWindowEx(
                    0,
                    _T("BUTTON"),  // Predefined class; Unicode assumed
                    _T("Select file"),      // Button text
                    WS_VISIBLE | WS_CHILD | BS_VCENTER | BS_CENTER,  // Styles
                    0,         // x position
                    0,         // y position
                    100,        // Button width
                    20,        // Button height
                    hWnd,     // Parent window
                    (HMENU)1,       // No menu.
                    GetModuleHandle(nullptr),  // Pointer not needed.
                    nullptr);      // Pointer not needed.

            hFont = CreateFont(
                    20,                     // Высота шрифта
                    0,                   // Ширина символа
                    0,                   // Угол наклона
                    0,                   // Угол поворота
                    FW_NORMAL,           // Ширина шрифта
                    FALSE,               // Курсив
                    FALSE,               // Подчеркнутый
                    FALSE,               // Зачеркнутый
                    DEFAULT_CHARSET,     // Кодировка
                    OUT_OUTLINE_PRECIS,  // Точность вывода
                    CLIP_DEFAULT_PRECIS, // Точность отсечения
                    CLEARTYPE_QUALITY,   // Качество вывода
                    VARIABLE_PITCH,      // Семейство шрифта
                    _T("Verdana"));        // Название шрифта

            if (hFont == nullptr)
            {
                MessageBoxW(hWnd, (L"Не удалось создать шрифт!"), L"Ошибка", MB_OK | MB_ICONERROR);
                return -1;
            }
            if (hwndButton == nullptr)
            {
                MessageBoxW(hWnd, L"Не удалось создать кнопку!", L"Ошибка", MB_OK | MB_ICONERROR);
            }

            break;
        }
        case WM_COMMAND:
        {
            if (LOWORD(wParam) == 1)
            {
                // Показываем диалоговое окно открытия файла
                OPENFILENAMEW ofn = {0};
                wchar_t szFileName[MAX_PATH + 1] = {0};

                ZeroMemory(&ofn, sizeof(ofn));
                ofn.lStructSize = sizeof(ofn);
                ofn.hwndOwner = hWnd;
                ofn.lpstrFilter = L"All Files (*.*)\0*.*\0Text Documents (*.txt)\0*.txt\0Word Documents (*.docx)\0*.docx\0PDF Documents (*.pdf)\0*.pdf\0";
                ofn.lpstrFile = szFileName;
                ofn.nMaxFile = MAX_PATH;
                ofn.Flags = OFN_EXPLORER | OFN_FILEMUSTEXIST | OFN_HIDEREADONLY;

//                if (GetOpenFileNameW(&ofn))
//                {
//                    std::string args = "python " + std::string("\"") + std::wstring_convert<std::codecvt_utf8<wchar_t>>().to_bytes(fullPath) + std::string("\" \"") +
//                            std::wstring_convert<std::codecvt_utf8<wchar_t>>().to_bytes(szFileName) + std::string("\"");
//                    std::thread thread(std::system, args.c_str());
//                    thread.join();
//                }
                if (GetOpenFileNameW(&ofn))
                {
                    STARTUPINFOW si;
                    ZeroMemory( &si, sizeof(si) );
                    si.cb = sizeof(si);

                    PROCESS_INFORMATION pi;
                    ZeroMemory( &pi, sizeof(pi) );

                    std::wstring args = L"\"";
                    args.append(fullPath);
                    args.append(L"\" \"");
                    args.append(szFileName);
                    args.append(L"\"");

                    wchar_t *command = const_cast<wchar_t *>(args.c_str());


                    if(!CreateProcessW(
                            fullPath.c_str(),
                            command,
                            NULL,
                            NULL,
                            FALSE,
                            0,
                            NULL,
                            NULL,
                            &si,
                            &pi))
                    {
                        printf( "CreateProcess failed (%d).\n", GetLastError() );
                    }

                    WaitForSingleObject( pi.hProcess, INFINITE );
                    CloseHandle( pi.hProcess );
                    CloseHandle( pi.hThread );
                }
            }
            break;
        }
        case WM_SIZE:
        {
            int width = LOWORD(lParam);
            int height = HIWORD(lParam);
            SetWindowPos(hwndButton, nullptr, width / 2 - 50, height - 75, 0, 0, SWP_NOSIZE | SWP_NOZORDER);

            x = width / 2 - 215;
            y = height / 2 - 200;
            InvalidateRect(hWnd, nullptr, TRUE);
            break;
        }
        case WM_DESTROY:
            if (hFont != nullptr)
            {
                DeleteObject(hFont);
            }

            PostQuitMessage(0);
            break;
        default:
            return DefWindowProc(hWnd, message, wParam, lParam);
    }

    return 0;
}