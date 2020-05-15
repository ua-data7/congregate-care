import React from 'react';

import {
    Typography, Toolbar, TablePagination,
    Checkbox, TableContainer, Table, TableHead,
    TableBody, TableRow, TableCell,
    Paper, TableSortLabel
} from '@material-ui/core';

export default function FacilityTable({facilities, selected, setSelected, total, cursor, setCursor}) {
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
            label: 'Name',
            key: 'name'
        },
        {
            label: 'Address',
            key: 'address'
        },
        {
            label: 'Phone',
            key: 'phones'    
        },
        {
            label: 'Email',
            key: 'emails'
        },
        {
            label: 'Last Reported',
            key: 'last_upload_date'
        },
        {
            label: 'Last Messaged',
            key: 'last_message_date'
        }
    ];

    return (
        <Paper>
            <Toolbar>
                <Typography variant="h6" component="h2" display="block">Facilities</Typography>
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
                        {facilities.map(facility => ((
                            <TableRow
                                hover
                                onClick={() => handleClick(facility.id)}
                                role="checkbox"
                                tabIndex={-1}
                                key={facility.id}
                                selected={selected.indexOf(facility.id) !== -1}
                            >
                                <TableCell padding="checkbox">
                                    <Checkbox checked={selected.indexOf(facility.id) !== -1}/>
                                </TableCell>
                                <TableCell>{facility.name}</TableCell>
                                <TableCell>{facility.address}</TableCell>
                                <TableCell>{facility.phones}</TableCell>
                                <TableCell>{facility.emails}</TableCell>
                                <TableCell>{facility.last_upload_date || 'Never'}</TableCell>
                                <TableCell>{facility.last_message_date || 'Never'}</TableCell>
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
