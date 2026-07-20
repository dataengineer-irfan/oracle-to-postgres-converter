import React, { useMemo } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import ActionToolbar from '../../common/ActionToolbar';

export default function DataPreviewTab({ tab }) {
  const rowData = [
    { p_sys_id: 4500001, p_fst_nm: 'John', p_lst_nm: 'Doe', p_npi: '1023456789', g_aud_ts: '2026-07-20 20:25:35' },
    { p_sys_id: 4500002, p_fst_nm: 'Jane', p_lst_nm: 'Smith', p_npi: '1987654321', g_aud_ts: '2026-07-20 20:25:35' },
    { p_sys_id: 4500003, p_fst_nm: 'Robert', p_lst_nm: 'Johnson', p_npi: '1554433221', g_aud_ts: '2026-07-20 20:25:35' },
    { p_sys_id: 4500004, p_fst_nm: 'Emily', p_lst_nm: 'Davis', p_npi: '1122334455', g_aud_ts: '2026-07-20 20:25:35' },
    { p_sys_id: 4500005, p_fst_nm: 'Michael', p_lst_nm: 'Wilson', p_npi: '1998877665', g_aud_ts: '2026-07-20 20:25:35' },
  ];

  const columnDefs = [
    { field: 'p_sys_id', headerName: 'ID', sortable: true, filter: true, width: 120 },
    { field: 'p_fst_nm', headerName: 'First Name', sortable: true, filter: true },
    { field: 'p_lst_nm', headerName: 'Last Name', sortable: true, filter: true },
    { field: 'p_npi', headerName: 'NPI', sortable: true, filter: true, width: 150 },
    { field: 'g_aud_ts', headerName: 'Audit Timestamp', sortable: true, filter: true, width: 200 },
  ];

  const defaultColDef = useMemo(() => ({
    resizable: true,
    sortable: true,
  }), []);

  return (
    <div className="h-full flex flex-col bg-bg">
      <ActionToolbar 
        title={`${tab.title} - Sample Data`} 
        onCopy={() => {}} 
        onDownload={() => {}} 
        type="CSV" 
      />
      <div className="flex-1 ag-theme-alpine-dark">
        <AgGridReact
          rowData={rowData}
          columnDefs={columnDefs}
          defaultColDef={defaultColDef}
          animateRows={true}
          rowSelection="multiple"
        />
      </div>
    </div>
  );
}
