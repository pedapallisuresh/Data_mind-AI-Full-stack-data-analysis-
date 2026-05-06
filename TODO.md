# TODO: Dataset Management & Visualization

## Task: Add visualization charts and modify upload dialog for multiple datasets

### Steps:
1. [x] Update backend (api.py) - Add multi-dataset support with endpoints
2. [x] Install Recharts library in frontend
3. [x] Update frontend (App.jsx) - Modify upload dialog to show previous datasets
4. [x] Add Visualizations tab with charts
5. [x] Update CSS styles for new components
6. [x] Test the implementation

### Summary of Changes:
- **Backend**: Modified data_store to hold multiple datasets with unique IDs
- **Endpoints Added**:
  - `/datasets` - List all datasets
  - `/datasets/switch` - Switch active dataset
  - `/datasets/delete` - Delete a dataset
  - `/visualization-data` - Get data for charts

- **Frontend**: 
  - Added dataset selector in upload tab
  - New Visualizations tab with charts
  - Charts: Histogram, Bar Chart, Correlation Heatmap, Box Plot
- **Charts**: Using Recharts library for visualization

