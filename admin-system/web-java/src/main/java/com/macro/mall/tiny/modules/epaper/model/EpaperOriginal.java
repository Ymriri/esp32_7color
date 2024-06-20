package com.macro.mall.tiny.modules.epaper.model;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.io.Serializable;
import java.util.Date;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Getter;
import lombok.Setter;

/**
 * <p>
 * 
 * </p>
 *
 * @author Ymri
 * @since 2024-04-06
 */
@Getter
@Setter
@TableName("epaper_original")
@Schema(name = "EpaperOriginal", description = "")
public class EpaperOriginal implements Serializable {

    private static final long serialVersionUID = 1L;

    @Schema(description = "文件唯一标识")
    @TableId(value = "file_id", type = IdType.AUTO)
    private Integer fileId;

    @Schema(description = "标题")
    private String title;

    private String description;

    @Schema(description = "图片地址")
    private String picPath;

    @Schema(description = "更新时间")
    private Date updateTime;

    @Schema(description = "关键字")
    private String keyword;


}
