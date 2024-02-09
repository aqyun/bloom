<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class DetikNewsClustered extends Model
{
    use HasFactory;

    protected $table = 'detiknews_clustered';

    protected $fillable = [
        'Id',
        'Kategori',
        'Judul',
        'Tanggal_dan_Waktu_Terbit',
        'Penulis',
        'Isi_Berita',
        'Cluster',
    ];
}
