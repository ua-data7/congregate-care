import React from 'react';
import axios from 'axios';

import {
    Grid, Container,
    Typography, Toolbar, TablePagination,
    Checkbox, TableContainer, Table, TableHead,
    TableBody, TableRow, TableCell, Button,
    Paper, TableSortLabel
} from '@material-ui/core';

import FacilityTable from './FacilityTable';

export default function SummaryDashboard() {
    const [dbState, setDbState] = React.useState({
        loading: true,
        error: false,
        facilities: [],
        total: 0
    });

    const [filters, setFilters] = React.useState({
        page: 1,
        liaisons: []
    });

    function handleChangePage(event, page) {
        setFilters(prev => ({
            ...prev, page: page + 1
        }));
    }

    React.useEffect(() => {
        axios.get('/api/facilities', {
            params: filters
        }).then(res => {
            setDbState(prev => ({...prev,
                loading: false,
                facilities: res.data.results,
                total: res.data.count
            }));
        }).catch(error => {
            setDbState(prev => ({...prev,
                loading: false,
                error: true
            }));
        });

        setDbState(prev => ({...prev,
            loading: true
        }));
        
    }, [filters]);

    return (
        <Container maxWidth="lg">
            <Grid container spacing={3} style={{marginTop: '80px'}}>
                <Grid item xs={6}>
                    <Paper>
                        <Toolbar>
                            <Typography variant="h6" component="h2" display="block">Late Reports</Typography>
                            <Typography style={{flexGrow: 1, marginLeft: '50px'}} variant="subtitle1" component="p">Showing facilities who haven't reported in the last 7 days.</Typography>
                        </Toolbar>
                        <TableContainer>
                            <Table>
                                <TableBody>
                                    {dbState.facilities.map(facility => (
                                        <TableRow
                                            hover
                                            role="checkbox"
                                            tabIndex={-1}
                                            key={facility.id}
                                        >
                                            <TableCell>{facility.name}</TableCell>
                                            <TableCell>{facility.phones}</TableCell>
                                            <TableCell>{facility.emails}</TableCell>
                                            <TableCell>{facility.last_upload_date || 'Never'}</TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
                        <TablePagination
                            component="div"
                            count={dbState.total}
                            rowsPerPage={10}
                            page={filters.page-1}
                            onChangePage={handleChangePage}
                            rowsPerPageOptions={[]}
                        />
                    </Paper>
                </Grid>
            </Grid>
        </Container>
    );
}
