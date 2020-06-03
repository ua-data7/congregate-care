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

    const liasons = [
        'Deb',
        'Allison',
        'Janet',
        'Kat',
        'Gabby',
        'Emerson',
        'Lisa',
        'Said',
        'Melody',
        'Justin',
        'Clementina'
    ];

    const tags = [
        'Apartments',
        'ALF',
        'LTC',
        'Other'
    ]

    return (
        <Paper>
            <Toolbar>
                <Typography variant="h6" component="h2">Filters</Typography>
            </Toolbar>
            <Toolbar>
                <Grid item xs={2}>
                    <Typography>Liason:</Typography>
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
                                    liasons: liasons || []
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
            </Toolbar>
            <Toolbar>
                <Grid item xs={2}>
                    <Typography>Submission date:</Typography>
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
                <Grid item xs={2}>
                    <Typography>Facility type:</Typography>
                </Grid>
                <Grid item xs={3}>
                    <FormControl style={{minWidth: '150px', maxWidth: '250px'}}>
                        <Select
                            labelId="category-label"
                            value={filters.category}
                            onChange={event => {
                                let cat = event.target.value;
                                setFilters(prev => ({
                                    ...prev,
                                    category: cat
                                }));
                            }}
                            input={<Input />}
                        >
                            <MenuItem value="all">All Categories</MenuItem>
                            <MenuItem value="cluster">Cluster</MenuItem>
                            <MenuItem value="noncluster">Non-Cluster</MenuItem>
                        </Select>
                    </FormControl>
                </Grid>
                <Grid item xs={3}>
                    <FormControl style={{minWidth: '150px', maxWidth: '250px'}}>
                        <Select
                            labelId="size-label"
                            value={filters.size}
                            onChange={event => {
                                let size = event.target.value;
                                setFilters(prev => ({
                                    ...prev,
                                    size: size
                                }));
                            }}
                            input={<Input />}
                        >
                            <MenuItem value="all">All Sizes</MenuItem>
                            <MenuItem value="Small">Small</MenuItem>
                            <MenuItem value="Large">Large</MenuItem>
                        </Select>
                    </FormControl>
                </Grid>
                <Grid item xs={3}>
                    <FormControl style={{minWidth: '150px', maxWidth: '250px'}}>
                        <InputLabel id="tags-label">Tags</InputLabel>
                        <Select
                            labelId="tags-label"
                            multiple
                            value={filters.tags}
                            onChange={event => {
                                let tags = event.target.value;    
                                setFilters(prev => ({
                                    ...prev,
                                    tags: tags || []
                                }));
                            }}
                            input={<Input />}
                            renderValue={(selected) => selected.join(', ')}
                        >
                        {tags.map((tag) => (
                            <MenuItem key={tag} value={tag}>
                                <Checkbox checked={filters.tags.indexOf(tag) !== -1} />
                                {tag}
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
                        label="Reporting New Cases"
                    />
                </Grid>
            </Toolbar>
            
        </Paper>
    );
}
