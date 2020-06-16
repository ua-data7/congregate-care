import React from 'react';
import axios from 'axios';

import {
    Typography, Toolbar, TablePagination, Dialog,
    Checkbox, TableContainer, Table, TableHead,
    TableBody, TableRow, TableCell, Button,
    Paper, TableSortLabel
} from '@material-ui/core';

import MessageSender from './MessageSender';

export default function SubmissionTable({submissions, total, cursor, setCursor, filters}) {

    const [selected, setSelected] = React.useState([]);
    const [recipients, setRecipients] = React.useState([]);
    const [modalOpen, setModalOpen] = React.useState(false);
    const closeModal = () => setModalOpen(false);

    function messageAll() {
        axios.get('/api/emails', {
            params: {
                ...filters
            }
        }).then(res => {
            setRecipients(res.data);
            setModalOpen(true);
        });
    }

    function messageSelected() {
        setRecipients(selected);
        setModalOpen(true);
    }
    
    function selectedIndex(facility) {
        if (!facility) return -1;
        for (let i = 0; i < selected.length; i++) {
            if (facility.id === selected[i].id) return i;
        }
        return -1;
    }

    function select(facility) {
        if (!facility) return;
        let index = selectedIndex(facility)
        if (index === -1) {
            setSelected(selected.concat([facility]));
        } else {
            setSelected(
                selected.slice(0, index)
                .concat(selected.slice(index + 1))
            )
        }
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
                <Typography variant="h6" component="h2" display="block">Submissions</Typography>
                <Typography style={{flexGrow: 1, marginLeft: '50px'}} variant="subtitle1" component="p">
                    Click on a column header to resort.
                </Typography>
                { selected.length > 0 &&
                    <Button style={{marginRight: '20px'}} variant="contained" color="secondary" onClick={messageSelected}>
                        Message selected
                    </Button>
                }
                <Button variant="contained" color="secondary" onClick={messageAll}>Message all</Button>
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
                        {submissions.map(row => (
                            <TableRow
                                hover
                                onClick={() => select(row.facility)}
                                role="checkbox"
                                tabIndex={-1}
                                key={row.id}
                                selected={selectedIndex(row.facility) !== -1}
                            >
                                <TableCell padding="checkbox">
                                    <Checkbox checked={selectedIndex(row.facility) !== -1}/>
                                </TableCell>
                                <TableCell>
                                    {row.facility ? row.facility.name :
                                        <React.Fragment>
                                            {row.facility_name} <strong>(Missing facility ID)</strong>
                                        </React.Fragment>
                                    }
                                </TableCell>
                                <TableCell>{row.facility && row.facility.address}</TableCell>
                                <TableCell>{row.facility && row.facility.phones}</TableCell>
                                <TableCell>{row.facility && row.facility.emails}</TableCell>
                                <TableCell>{row.reported_new_cases ? 'Yes' : 'No'}</TableCell>
                                <TableCell>{row.created_date || 'Never'}</TableCell>
                            </TableRow>
                        ))}
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
            <MessageSender open={modalOpen} onClose={closeModal} recipients={recipients} closeModal={closeModal}/>
        </Paper>
    );
}
