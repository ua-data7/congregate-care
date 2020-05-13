import React from 'react';

import {
    Typography, Toolbar,
    Checkbox, TableContainer, Table, TableHead,
    TableBody, TableRow, TableCell,
    Paper, TableSortLabel
} from '@material-ui/core';

export default function SubmissionTable({submissions, selected, setSelected, order, setOrder}) {
    function handleClick (id) {
        let selectedIndex = selected.indexOf(id);
        let newSelected = [];
    
        if (selectedIndex === -1) {
            newSelected = newSelected.concat(selected, id);
        } else if (selectedIndex === 0) {
            newSelected = newSelected.concat(selected.slice(1));
        } else if (selectedIndex === selected.length - 1) {
            newSelected = newSelected.concat(selected.slice(0, -1));
        } else if (selectedIndex > 0) {
            newSelected = newSelected.concat(
                selected.slice(0, selectedIndex),
                selected.slice(selectedIndex + 1),
            );
        }
        setSelected(newSelected);
    }

    function handleSort(key) {
        if (order.indexOf(key) !== -1) {
            if (order.charAt(0) === '-') {
                setOrder(key);
            } else {
                setOrder('-' + key);
            }
        } else {
            setOrder(key);
        }
    }

    let sortKeys = [
        {
            label: 'Facility',
            key: 'facility__name'
        },
        {
            label: 'Address',
            key: 'facility__address'
        },
        {
            label: 'Phone',
            key: 'facility__phones'    
        },
        {
            label: 'Email',
            key: 'facility__emails'
        },
        {
            label: 'End Date',
            key: 'created_date'
        }
    ];

    return (
        <Paper>
            <Toolbar>
                <Typography variant="h6" component="h2">Submissions</Typography>
            </Toolbar>
            <TableContainer>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell padding="checkbox"></TableCell>
                            {sortKeys.map(sortKey => (
                                <TableCell key={sortKey.key}>
                                    <TableSortLabel
                                        active={order.indexOf(sortKey.key) !== -1}
                                        direction={order.charAt(0) === '-' ? 'desc' : 'asc'}
                                        onClick={() => handleSort(sortKey.key)}
                                    >
                                        {sortKey.label}
                                    </TableSortLabel>
                                </TableCell>
                            ))}
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {submissions.map(row => ((
                            <TableRow
                                hover
                                onClick={() => handleClick(row.id)}
                                role="checkbox"
                                tabIndex={-1}
                                key={row.id}
                                selected={selected.indexOf(row.id) !== -1}
                            >
                                <TableCell padding="checkbox">
                                    <Checkbox checked={selected.indexOf(row.id) !== -1}/>
                                </TableCell>
                                <TableCell>{row.facility.name}</TableCell>
                                <TableCell>{row.facility.address}</TableCell>
                                <TableCell>{row.facility.phones}</TableCell>
                                <TableCell>{row.facility.emails}</TableCell>
                                <TableCell>{row.created_date}</TableCell>
                            </TableRow>
                        )))}
                    </TableBody>
                </Table>
            </TableContainer>
        {/*
        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={rows.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onChangePage={handleChangePage}
          onChangeRowsPerPage={handleChangeRowsPerPage}
        /> */}
        </Paper>
    );
}
