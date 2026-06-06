// mock-react-structure.txt
// This is a blueprint of the React Dashboard components
Components:
- Layout/
  - Sidebar.tsx (Navigation: Dashboard, Profiles, Allowlist, Reports)
  - Header.tsx (User status, Global settings)
- Dashboard/
  - EventLogTable.tsx (Columns: Timestamp, Child, URL, Category, Decision, Action)
  - StatsOverview.tsx (Cards: Total Blocks, Most Blocked Category, Time Activity)
- Profiles/
  - ProfileEditor.tsx (Age, Band selection, Custom threshold sliders)
  - ProfileList.tsx (Grid of child profiles)
- Allowlist/
  - PatternManager.tsx (Input for regex/domain, delete/edit options)
- Reports/
  - WeeklyTrendChart.tsx (Line chart of blocks over 7 days)
  - PDFExportButton.tsx (Triggers API report generation)
