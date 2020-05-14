import React from 'react';
import axios from 'axios';

import {
    Grid, Container
} from '@material-ui/core';

import FacilityTable from './FacilityTable';
import DashboardFilters from './DashboardFilters';
import MessageSender from './MessageSender';

export default function Dashboard() {
    const [dbState, setDbState] = React.useState({
        loading: true,
        error: false,
        facilities: [],
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
        axios.get('/api/facilities', {
            params: {
                ...filters,
                order
            }
        }).then(res => {
            setDbState(prev => ({...prev,
                loading: false,
                facilities: res.data
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
                    <FacilityTable
                        loading={dbState.loading}
                        facilities={dbState.facilities}
                        selected={selected}
                        setSelected={setSelected}
                        order={order}
                        setOrder={setOrder}
                    />
                </Grid>
                <Grid item xs={12}>
                    <MessageSender selected={selected} />
                </Grid>
            </Grid>
        </Container>
    );
}
