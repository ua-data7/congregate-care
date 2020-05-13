import React from 'react';
import axios from 'axios';

import {
    Typography, Grid, Toolbar, Container, CssBaseline,
    Checkbox, FormControlLabel, TableContainer, Table, TableHead,
    TableBody, TableRow, Input, TableCell, AppBar, makeStyles,
    TablePagination, Paper
} from '@material-ui/core';
import MaskedInput from 'react-text-mask';


function DateInput(props) {
    let { inputRef, ...other } = props;
    return (
        <MaskedInput {...other}
            mask={[/\d/, /\d/, '/', /\d/, /\d/, '/', /\d/, /\d/, /\d/, /\d/]}
            placeholder="MM/DD/YYYY"
            placeholderChar={'\u2000'}
        />
    )
}

const useStyles = makeStyles(theme => ({
    appBarSpacer: theme.mixins.toolbar,
    grayed: {
        color: '#555555'
    }
}));

export default function Dashboard() {
    const [dbState, setDbState] = React.useState({
        loading: true,
        error: false,
        submissions: [],
        filters: {}
    });

    const [filters, setFilters] = React.useState({
        minDate: null,
        maxDate: null,
        newCases: false,
        reportedAfter: null,
        liasons: [],
        size: null
    });

    const [selected, setSelected] = React.useState([]);

    React.useEffect(() => {
        axios.get('/api/submissions', {
            params: filters
        }).then(res => {
            setDbState(prev => ({...prev,
                loading: false,
                submissions: res.data
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

    const classes = useStyles();

    return (
        <React.Fragment>
            <CssBaseline />
            <AppBar>
                <Toolbar>
                    <Typography component="h1" variant="h6" noWrap>
                        PCHD Qualtrics Submissions
                    </Typography>
                </Toolbar>
            </AppBar>
            <div className={classes.appBarSpacer} />
            <Container maxWidth="lg">
                <Grid container spacing={3}>
                    <Grid item xs={12}>
                        <DashboardFilters loading={dbState.loading} filters={filters} setFilters={setFilters} />
                    </Grid>
                    <Grid item xs={12}>
                        <SubmissionTable loading={dbState.loading} submissions={dbState.submissions} selected={selected} setSelected={setSelected}/>
                    </Grid>
                </Grid>
            </Container>
        </React.Fragment>
    );
}

function SubmissionTable({submissions, selected, setSelected}) {
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

    return (
        <Paper>
            <Toolbar>
                <Typography variant="h6" component="h2">Submissions</Typography>
            </Toolbar>
            <TableContainer>
                <Table>
                    {/* <EnhancedTableHead
                        classes={classes}
                        numSelected={selected.length}
                        order={order}
                        orderBy={orderBy}
                        onSelectAllClick={handleSelectAllClick}
                        onRequestSort={handleRequestSort}
                        rowCount={rows.length}
                    /> */}
                    <TableHead>
                        <TableRow>
                            <TableCell>Facility</TableCell>
                            <TableCell>Address</TableCell>
                            <TableCell>Phone</TableCell>
                            <TableCell>Email</TableCell>
                            <TableCell>End&nbsp;Date</TableCell>
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
        {/* TablePagination goes here
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


function DashboardFilters({filters, setFilters, loading}) {
    return (
        <Paper>
            <Toolbar>
                <Typography variant="h6" component="h2">Filters</Typography>
            </Toolbar>
            <Toolbar>
                <Grid item xs={1}>
                    <Typography>Date range:</Typography>
                </Grid>
                <Grid item xs={2}>
                    <Input
                        value={filters.minDate}
                        onChange={event =>  {
                            if (event.target.value === '' || !event.target.value.includes('\u2000')) {
                                let date = event.target.value;    
                                setFilters(prev => ({
                                    ...prev,
                                    minDate: date || null
                                }));
                            }
                        }}
                        name="minDate"
                        inputComponent={DateInput}
                        disabled={loading}
                    />
                </Grid>
                <Grid item xs={1}>
                    <Typography align="center">to</Typography>
                </Grid>
                <Grid item xs={2}>
                    <Input
                        value={filters.maxDate}
                        onChange={event =>  {
                            if (event.target.value === '' || !event.target.value.includes('\u2000')) {
                                let date = event.target.value;    
                                setFilters(prev => ({
                                    ...prev,
                                    maxDate: date || null
                                }));
                            }
                        }}
                        name="maxDate"
                        inputComponent={DateInput}
                        disabled={loading}
                    />
                </Grid>
            </Toolbar>
            <Toolbar>
                <Grid item xs={1}>
                    <Typography>Filter:</Typography>
                </Grid>
                <Grid item xs={2}>
                    <FormControlLabel
                        control={<Checkbox
                            checked={filters.newCases}
                            onChange={event => {
                                let checked = event.target.checked;
                                setFilters(prev => ({
                                    ...prev,
                                    newCases: checked
                                }));
                            }}
                            name="newCases"
                            disabled={loading} 
                        />}
                        label="New Cases"
                    />
                </Grid>
            </Toolbar>
        </Paper>
    );
}
