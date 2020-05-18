import React from 'react';

import {
    Typography, Toolbar, TablePagination,
    Checkbox, TableContainer, Table, TableHead,
    TableBody, TableRow, TableCell,
    Paper, TableSortLabel
} from '@material-ui/core';

export default function SubmissionTable({submissions, selected, setSelected, cursor, setCursor, total}) {
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
        if (cursor.order.indexOf(key) !== -1) {
            if (cursor.order.charAt(0) === '-') {
                setCursor(prev => ({...prev,
                    order: key
                }));
            } else {
                setCursor(prev => ({...prev,
                    order: '-' + key
                }));
            }
        } else {
            setCursor(prev => ({...prev,
                order: key
            }));
        }
    }

    function handleChangePage(event, page) {
        setCursor(prev => ({
            ...prev, page
        }));
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
            label: 'New Cases?',
            key: 'reported_new_cases'
        },
        {
            label: 'Upload Date',
            key: 'created_date'
        }
    ];

    return (
        <Paper>
            <Toolbar>
                <Typography variant="h6" component="h2">Submissions</Typography>
                <Typography variant="subtitle1" component="p" style={{marginLeft: '50px'}}>Click on a column header to resort.</Typography>
            </Toolbar>
            <TableContainer>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell padding="checkbox"></TableCell>
                            {sortKeys.map(sortKey => (
                                <TableCell key={sortKey.key}>
                                    <TableSortLabel
                                        active={cursor.order.indexOf(sortKey.key) !== -1}
                                        direction={cursor.order.charAt(0) === '-' ? 'desc' : 'asc'}
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
                                <TableCell>{row.reported_new_cases ? 'Yes' : 'No'}</TableCell>
                                <TableCell>{row.created_date || 'Never'}</TableCell>
                            </TableRow>
                        )))}
                    </TableBody>
                </Table>
            </TableContainer>
            <TablePagination
                component="div"
                count={total}
                rowsPerPage={10}
                page={cursor.page}
                onChangePage={handleChangePage}
                rowsPerPageOptions={[]}
            />
        </Paper>
    );
}
