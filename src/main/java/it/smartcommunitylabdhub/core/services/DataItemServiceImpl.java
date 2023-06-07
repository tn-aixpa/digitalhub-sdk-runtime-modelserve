package it.smartcommunitylabdhub.core.services;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

import it.smartcommunitylabdhub.core.exceptions.CoreException;
import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.converters.CommandFactory;
import it.smartcommunitylabdhub.core.models.dtos.DataItemDTO;
import it.smartcommunitylabdhub.core.models.entities.DataItem;
import it.smartcommunitylabdhub.core.repositories.DataItemRepository;
import it.smartcommunitylabdhub.core.services.builders.dtos.DataItemDTOBuilder;
import it.smartcommunitylabdhub.core.services.builders.entities.DataItemEntityBuilder;
import it.smartcommunitylabdhub.core.services.interfaces.DataItemService;

@Service
public class DataItemServiceImpl implements DataItemService {

    private final DataItemRepository dataItemRepository;
    private final CommandFactory commandFactory;

    public DataItemServiceImpl(
            DataItemRepository dataItemRepository,
            CommandFactory commandFactory) {
        this.dataItemRepository = dataItemRepository;
        this.commandFactory = commandFactory;

    }

    @Override
    public List<DataItemDTO> getDataItems(Pageable pageable) {
        try {
            Page<DataItem> dataItemPage = this.dataItemRepository.findAll(pageable);
            return dataItemPage.getContent().stream().map((dataItem) -> {
                return new DataItemDTOBuilder(commandFactory, dataItem, false).build();
            }).collect(Collectors.toList());
        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }

    }

    @Override
    public DataItemDTO createDataItem(DataItemDTO dataItemDTO) {
        try {
            // Build a dataItem and store it on db
            final DataItem dataItem = new DataItemEntityBuilder(commandFactory, dataItemDTO).build();
            this.dataItemRepository.save(dataItem);

            // Return dataItem DTO
            return new DataItemDTOBuilder(
                    commandFactory,
                    dataItem, false).build();

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public DataItemDTO getDataItem(String uuid) {
        return dataItemRepository.findById(uuid)
                .map(dataItem -> {
                    try {
                        return new DataItemDTOBuilder(commandFactory, dataItem, false).build();
                    } catch (CustomException e) {
                        throw new CoreException(
                                "InternalServerError",
                                e.getMessage(),
                                HttpStatus.INTERNAL_SERVER_ERROR);
                    }
                })
                .orElseThrow(() -> new CoreException(
                        "DataItemNotFound",
                        "The dataItem you are searching for does not exist.",
                        HttpStatus.NOT_FOUND));
    }

    @Override
    public DataItemDTO updateDataItem(DataItemDTO dataItemDTO, String uuid) {
        if (!dataItemDTO.getId().equals(uuid)) {
            throw new CoreException(
                    "DataItemNotMatch",
                    "Trying to update a DataItem with a UUID different from the one passed in the request.",
                    HttpStatus.NOT_FOUND);
        }

        return dataItemRepository.findById(uuid)
                .map(dataItem -> {
                    try {
                        DataItemEntityBuilder dataItemBuilder = new DataItemEntityBuilder(commandFactory, dataItemDTO);
                        DataItem dataItemUpdated = dataItemBuilder.update(dataItem);
                        dataItemRepository.save(dataItemUpdated);
                        return new DataItemDTOBuilder(commandFactory, dataItemUpdated, false).build();
                    } catch (CustomException e) {
                        throw new CoreException(
                                "InternalServerError",
                                e.getMessage(),
                                HttpStatus.INTERNAL_SERVER_ERROR);
                    }
                })
                .orElseThrow(() -> new CoreException(
                        "DataItemNotFound",
                        "The dataItem you are searching for does not exist.",
                        HttpStatus.NOT_FOUND));
    }

    @Override
    public boolean deleteDataItem(String uuid) {
        try {
            if (this.dataItemRepository.existsById(uuid)) {
                this.dataItemRepository.deleteById(uuid);
                return true;
            }
            throw new CoreException(
                    "DataItemNotFound",
                    "The dataItem you are trying to delete does not exist.",
                    HttpStatus.NOT_FOUND);
        } catch (Exception e) {
            throw new CoreException(
                    "InternalServerError",
                    "cannot delete dataItem",
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

}
