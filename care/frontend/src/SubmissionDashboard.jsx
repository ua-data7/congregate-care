import React from 'react';
import axios from 'axios';

import {
    Grid, Container
} from '@material-ui/core';

import SubmissionTable from './SubmissionTable';
import DashboardFilters from './DashboardFilters';
import MessageSender from './MessageSender';

export default function SubmissionDashboard({classes}) {
    const [dbState, setDbState] = React.useState({
        loading: true,
        error: false,
        submissions: [],
        total: 0,
        filters: {}
    });

    const [filters, setFilters] = React.useState({
        minDate: null,
        maxDate: null,
        newCases: false,
        category: 'all',
        size: 'all',
        liasons: []
    });

    const [cursor, setCursor] = React.useState({
        order: 'created_date',
        page: 0
    });

    const [selected, setSelected] = React.useState([]);

    React.useEffect(() => {
        axios.get('/api/submissions', {
            params: {
                ...filters,
                page: cursor.page + 1,
                order: cursor.order
            }
        }).then(res => {
            setDbState(prev => ({...prev,
                loading: false,
                submissions: res.data.results,
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
        
    }, [filters, cursor]);

    return (
        <Container maxWidth="lg">
            <div className={classes.appBarSpacer} />
            <Grid container spacing={3}>
                <Grid item xs={12}>
                    <DashboardFilters loading={dbState.loading} filters={filters} setFilters={setFilters} />
                </Grid>
                <Grid item xs={12}>
                    <SubmissionTable
                        loading={dbState.loading}
                        submissions={dbState.submissions}
                        selected={selected}
                        setSelected={setSelected}
                        cursor={cursor}
                        setCursor={setCursor}
                        total={dbState.total}
                    />
                </Grid>
            </Grid>
        </Container>
    );
}
