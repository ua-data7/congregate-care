import React from 'react';
import axios from 'axios';

import {
    Grid, Container
} from '@material-ui/core';

import FacilityTable from './FacilityTable';
import DashboardFilters from './DashboardFilters';

export default function FacilityDashboard() {
    const [dbState, setDbState] = React.useState({
        loading: true,
        error: false,
        facilities: [],
        total: 0
    });

    const [filters, setFilters] = React.useState({
        minDate: null,
        maxDate: null,
        newCases: false,
        category: 'all',
        size: 'all',
        liaisons: [],
        tags: []
    });

    const [cursor, setCursor] = React.useState({
        order: 'name',
        page: 0
    });

    React.useEffect(() => {
        axios.get('/api/facilities', {
            params: {
                ...filters,
                page: cursor.page + 1,
                order: cursor.order
            }
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
        
    }, [filters, cursor]);

    return (
        <Container maxWidth="lg">
            <Grid container spacing={3} style={{marginTop: '80px'}}>
                <Grid item xs={12}>
                    <DashboardFilters
                        loading={dbState.loading}
                        filters={filters}
                        setFilters={setFilters}
                    />
                </Grid>
                <Grid item xs={12}>
                    <FacilityTable
                        loading={dbState.loading}
                        facilities={dbState.facilities}
                        total={dbState.total}
                        cursor={cursor}
                        setCursor={setCursor}
                        filters={filters}
                    />
                </Grid>
            </Grid>
        </Container>
    );
}
