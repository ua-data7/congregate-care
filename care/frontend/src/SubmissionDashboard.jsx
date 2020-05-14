import React from 'react';
import axios from 'axios';

import {
    Grid, Container
} from '@material-ui/core';

import SubmissionTable from './SubmissionTable';
import DashboardFilters from './DashboardFilters';
import MessageSender from './MessageSender';

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

    return (
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
    );
}
