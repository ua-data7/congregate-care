import React from 'react';
import axios from 'axios';

import {
    Typography, Grid, Toolbar, Container, CssBaseline,
    AppBar, makeStyles
} from '@material-ui/core';

import SubmissionTable from './SubmissionTable';
import DashboardFilters from './DashboardFilters';
import MessageSender from './MessageSender';


const useStyles = makeStyles(theme => ({
    appBarSpacer: theme.mixins.toolbar
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
        cluster: false,
        reportedAfter: null,
        liasons: [],
        size: null
    });

    const [selected, setSelected] = React.useState([]);
    const [order, setOrder] = React.useState('created_date');

    React.useEffect(() => {
        axios.get('/api/submissions', {
            params: {
                ...filters,
                order
            }
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
        
    }, [filters, order]);

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
                        <SubmissionTable loading={dbState.loading} submissions={dbState.submissions} selected={selected} setSelected={setSelected} order={order} setOrder={setOrder}/>
                    </Grid>
                    <Grid item xs={12}>
                        <MessageSender selected={selected} />
                    </Grid>
                </Grid>
            </Container>
        </React.Fragment>
    );
}
