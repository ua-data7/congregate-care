import React from 'react';

import {
    Typography, Grid, Toolbar,
    Checkbox, FormControlLabel, Input,
    Paper, FormControl, InputLabel, Select, MenuItem
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

export default function DashboardFilters({filters, setFilters, loading}) {

    let liasons = [
        'Deb Agristo',
        'Allison Burnett',
        'Janet Corley',
        'Kat Davis',
        'Gabby Flores',
        'Emerson Kuhn',
        'Lisa Longo',
        'Said Martinez',
        'Melody Mena',
        'Justin Tantoon',
        'Clementina'
    ];

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
                <Grid item xs={3}>
                    <FormControl style={{minWidth: '150px', maxWidth: '250px'}}>
                        <InputLabel id="liason-label">Liason</InputLabel>
                        <Select
                            labelId="liason-label"
                            multiple
                            value={filters.liasons}
                            onChange={event => {
                                let liasons = event.target.value;    
                                setFilters(prev => ({
                                    ...prev,
                                    liasons: liasons || null
                                }));
                            }}
                            input={<Input />}
                            renderValue={(selected) => selected.join(', ')}
                        >
                        {liasons.map((liason) => (
                            <MenuItem key={liason} value={liason}>
                                <Checkbox checked={filters.liasons.indexOf(liason) !== -1} />
                                {liason}
                            </MenuItem>
                        ))}
                        </Select>
                    </FormControl>
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
                <Grid item xs={2}>
                    <FormControlLabel
                        control={<Checkbox
                            checked={filters.cluster}
                            onChange={event => {
                                let checked = event.target.checked;
                                setFilters(prev => ({
                                    ...prev,
                                    cluster: checked
                                }));
                            }}
                            name="cluster"
                            disabled={loading} 
                        />}
                        label="Cluster"
                    />
                </Grid>
            </Toolbar>
        </Paper>
    );
}
